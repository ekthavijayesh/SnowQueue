from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "queue_wait_model.joblib"
DATA_PATH = BASE_DIR / "data" / "queue_waiting_time.csv"

app = Flask(__name__)

# The model expects these exact feature names.
FEATURE_COLUMNS = [
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

# Load the trained model and dataset once when the server starts.
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

required_columns = FEATURE_COLUMNS + ["wait_time_minutes"]
missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    raise ValueError(f"Dataset is missing columns: {missing_columns}")


@app.route("/")
def home():
    rides = sorted(df["ride_name"].dropna().unique().tolist())

    summary = {
        "ride_count": int(df["ride_name"].nunique()),
        "record_count": int(len(df)),
        "average_wait": round(float(df["wait_time_minutes"].mean()), 1),
    }

    ride_means = (
        df.groupby("ride_name")["wait_time_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    summary["rides"] = [
        {"name": str(name), "wait": round(float(wait), 1)}
        for name, wait in ride_means.items()
    ]

    return render_template(
        "index.html",
        rides=rides,
        summary=summary,
    )


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Please submit valid prediction inputs."}), 400

    try:
        ride_name = str(payload["ride_name"])
        hour = int(payload["hour"])
        day_type = str(payload["day_type"])
        weather = str(payload["weather"])
        queue_length = int(payload["queue_length"])
        ride_capacity = int(payload["ride_capacity"])
        ride_cycle_minutes = float(payload["ride_cycle_minutes"])
        park_attendance = int(payload["park_attendance"])
        temperature_c = float(payload["temperature_c"])

        if ride_name not in df["ride_name"].astype(str).unique():
            raise ValueError("Please choose a ride from the available list.")

        if not 9 <= hour <= 22:
            raise ValueError("Hour must be between 9 and 22.")

        if day_type not in ["Weekday", "Weekend"]:
            raise ValueError("Please choose Weekday or Weekend.")

        if weather not in ["Sunny", "Cloudy", "Rainy"]:
            raise ValueError("Please choose a valid weather condition.")

        if not 0 <= queue_length <= 1000:
            raise ValueError("Queue length must be between 0 and 1000.")

        if ride_capacity <= 0:
            raise ValueError("Ride capacity must be greater than zero.")

        if not 2 <= ride_cycle_minutes <= 8:
            raise ValueError("Ride cycle duration must be between 2 and 8 minutes.")

        if not 0 <= park_attendance <= 100000:
            raise ValueError("Park attendance must be between 0 and 100000.")

        if not 10 <= temperature_c <= 45:
            raise ValueError("Temperature must be between 10 and 45 °C.")

        input_data = pd.DataFrame([{
            "ride_name": ride_name,
            "hour": hour,
            "day_type": day_type,
            "weather": weather,
            "queue_length": queue_length,
            "ride_capacity": ride_capacity,
            "ride_cycle_minutes": ride_cycle_minutes,
            "park_attendance": park_attendance,
            "temperature_c": temperature_c,
            "is_peak_hour": int(12 <= hour <= 18),
        }], columns=FEATURE_COLUMNS)

        prediction = max(0.0, float(model.predict(input_data)[0]))

        if prediction < 15:
            category = "Short"
        elif prediction < 45:
            category = "Moderate"
        else:
            category = "Long"

        return jsonify({
            "wait_time": round(prediction, 1),
            "category": category,
            "ride_name": ride_name,
            "hour": hour,
            "disclaimer": (
                "Educational estimate based on synthetic data. "
                "Not a validated real-world forecast."
            ),
        })

    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "The model could not generate a prediction. "
                     "Check the server terminal for details."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
