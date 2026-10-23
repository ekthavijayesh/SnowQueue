
from pathlib import Path
import json
import shutil

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "queue_waiting_time.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "queue_wait_model.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

FEATURES = [
    "ride_name",
    "hour",
    "day_type",
    "weather",
    "queue_length",
    "ride_capacity",
    "ride_cycle_minutes",
    "park_attendance",
    "temperature_c",
    "is_peak_hour",
]
TARGET = "wait_time_minutes"

CATEGORICAL = ["ride_name", "day_type", "weather"]
NUMERIC = [col for col in FEATURES if col not in CATEGORICAL]


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    results = []
    best_pipeline = None
    best_name = None
    best_mae = float("inf")

    for name, estimator in {
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=200, random_state=42, n_jobs=-1
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=200, random_state=42, n_jobs=-1
        ),
    }.items():
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore"),
                    CATEGORICAL,
                ),
                ("numeric", "passthrough", NUMERIC),
            ]
        )

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", estimator),
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5
        r2 = r2_score(y_test, predictions)

        results.append({
            "model": name,
            "MAE": round(float(mae), 3),
            "RMSE": round(float(rmse), 3),
            "R2": round(float(r2), 4),
        })

        print(f"\n{name}")
        print(f"  MAE:  {mae:.2f} minutes")
        print(f"  RMSE: {rmse:.2f} minutes")
        print(f"  R²:   {r2:.4f}")

        if mae < best_mae:
            best_mae = mae
            best_name = name
            best_pipeline = pipeline

    print("\nModel comparison (lower MAE is better):")
    print(pd.DataFrame(results).sort_values("MAE").to_string(index=False))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Back up existing files before replacing them.
    if MODEL_PATH.exists():
        backup = MODEL_DIR / "queue_wait_model_backup.joblib"
        shutil.copy2(MODEL_PATH, backup)
        print(f"\nExisting model backed up to: {backup}")

    if METADATA_PATH.exists():
        metadata_backup = MODEL_DIR / "model_metadata_backup.json"
        shutil.copy2(METADATA_PATH, metadata_backup)
        print(f"Existing metadata backed up to: {metadata_backup}")

    # The saved Pipeline accepts the same feature-named DataFrame
    # that server.py currently passes to model.predict().
    joblib.dump(best_pipeline, MODEL_PATH)

    metadata = {
        "best_model": best_name,
        "target": TARGET,
        "features": FEATURES,
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "data_type": "synthetic educational dataset",
        "selection_metric": "MAE",
        "test_metrics": next(
            result for result in results if result["model"] == best_name
        ),
    }

    METADATA_PATH.write_text(
        json.dumps(metadata, indent=4),
        encoding="utf-8",
    )

    print(f"\nBest model saved: {MODEL_PATH}")
    print(f"Metadata saved: {METADATA_PATH}")
    print("\nEvaluation is based on synthetic data, not real park observations.")


if __name__ == "__main__":
    main()
