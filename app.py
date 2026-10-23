from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "queue_wait_model.joblib"

FEATURES = [
    "hour",
    "day_type",
    "weather",
    "queue_length",
    "ride_capacity",
    "ride_cycle_minutes",
    "park_attendance",
    "temperature_c",
    "ride_name",
    "is_peak_hour",
]


def load_model():
    if not MODEL_PATH.exists():
        app.logger.error("Model file not found: %s", MODEL_PATH)
        return None

    try:
        loaded_model = joblib.load(MODEL_PATH)
        app.logger.info("Model loaded successfully from %s", MODEL_PATH)
        return loaded_model
    except Exception:
        app.logger.exception("Could not load the trained model")
        return None


model = load_model()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "model_file": MODEL_PATH.name,
    })


@app.post("/predict")
def predict():
    if model is None:
        return jsonify({
            "error": (
                "The trained model could not be loaded. "
                "Check the terminal for the model-loading error."
            )
        }), 503

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please submit valid prediction data."
        }), 400

    try:
        ride_name = str(data.get("ride_name", "")).strip()
        day_type = str(data.get("day_type", "")).strip().lower()
        weather = str(data.get("weather", "")).strip().lower()

        if not ride_name:
            raise ValueError("Please select a ride.")

        if day_type not in {"weekday", "weekend"}:
            raise ValueError("Day type must be weekday or weekend.")

        if weather not in {"sunny", "cloudy", "rainy", "snowy"}:
            raise ValueError("Please select a supported weather condition.")

        hour = int(data["hour"])
        queue_length = int(data["queue_length"])
        ride_capacity = int(data["ride_capacity"])
        ride_cycle_minutes = float(data["ride_cycle_minutes"])
        park_attendance = int(data["park_attendance"])
        temperature_c = float(data["temperature_c"])

        if not 0 <= hour <= 23:
            raise ValueError("Hour must be between 0 and 23.")

        if queue_length < 0 or ride_capacity <= 0 or park_attendance < 0:
            raise ValueError(
                "Queue, capacity, or attendance values are invalid."
            )

        if ride_cycle_minutes <= 0:
            raise ValueError("Ride duration must be greater than zero.")

        if not -20 <= temperature_c <= 60:
            raise ValueError("Temperature must be between -20 and 60.")

        if not np.all(np.isfinite([
            ride_cycle_minutes,
            temperature_c,
        ])):
            raise ValueError("Please enter valid numeric values.")

        # Use the same feature names and raw categorical values
        # expected by the training pipeline.
        row = pd.DataFrame([{
            "hour": hour,
            "day_type": day_type,
            "weather": weather,
            "queue_length": queue_length,
            "ride_capacity": ride_capacity,
            "ride_cycle_minutes": ride_cycle_minutes,
            "park_attendance": park_attendance,
            "temperature_c": temperature_c,
            "ride_name": ride_name,
            "is_peak_hour": int(17 <= hour <= 20),
        }], columns=FEATURES)

        prediction = float(model.predict(row)[0])

        if not np.isfinite(prediction):
            raise ValueError("The model returned an invalid prediction.")

        wait_time = max(0, round(prediction, 1))

        if wait_time < 10:
            category = "Short wait"
        elif wait_time < 30:
            category = "Moderate wait"
        elif wait_time < 60:
            category = "Long wait"
        else:
            category = "Very long wait"

        return jsonify({
            "wait_time": wait_time,
            "category": category,
            "message": f"Estimated waiting time for {ride_name}.",
            "disclaimer": (
                "This is a model-based estimate, "
                "not a live queue measurement."
            ),
        })

    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return jsonify({"error": str(exc)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": (
                "Prediction failed. Check the terminal for details."
            )
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
