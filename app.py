
from pathlib import Path
import math
import os

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
    """Load the existing trained model without retraining it."""
    if not MODEL_PATH.is_file():
        app.logger.error("Model file not found: %s", MODEL_PATH)
        return None

    try:
        loaded_model = joblib.load(MODEL_PATH)
        app.logger.info("Trained model loaded successfully.")
        return loaded_model
    except Exception:
        app.logger.exception("Could not load the trained model.")
        return None


model = load_model()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    """Health endpoint for deployment checks."""
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "model_file": MODEL_PATH.name,
    }), 200 if model is not None else 503


@app.post("/predict")
def predict():
    """Validate user input and return a model-based wait-time estimate."""
    if model is None:
        return jsonify({
            "error": (
                "The trained model could not be loaded. "
                "Please check the server logs."
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

        # Parse numeric fields.
        def get_number(field, converter=float):
            value = data.get(field)

            if value is None or isinstance(value, bool):
                raise ValueError(f"Please enter a valid value for {field}.")

            try:
                number = converter(value)
            except (ValueError, TypeError, OverflowError):
                raise ValueError(
                    f"Please enter a valid value for {field}."
                ) from None

            if isinstance(number, float) and not math.isfinite(number):
                raise ValueError(f"{field} must be a finite number.")

            return number

        hour = get_number("hour", int)
        queue_length = get_number("queue_length", int)
        ride_capacity = get_number("ride_capacity", int)
        ride_cycle_minutes = get_number("ride_cycle_minutes", float)
        park_attendance = get_number("park_attendance", int)
        temperature_c = get_number("temperature_c", float)

        if not 0 <= hour <= 23:
            raise ValueError("Hour must be between 0 and 23.")

        if queue_length < 0:
            raise ValueError("Queue length cannot be negative.")

        if ride_capacity <= 0:
            raise ValueError("Ride capacity must be greater than zero.")

        if park_attendance < 0:
            raise ValueError("Park attendance cannot be negative.")

        if ride_cycle_minutes <= 0:
            raise ValueError("Ride cycle must be greater than zero.")

        if not -20 <= temperature_c <= 60:
            raise ValueError("Temperature must be between -20 and 60.")

        # Preserve the feature order and names used during model training.
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
        }), 200

    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return jsonify({"error": str(exc)}), 400

    except Exception:
        app.logger.exception("Prediction failed.")
        return jsonify({
            "error": "Prediction failed. Please try again later."
        }), 500


if __name__ == "__main__":
    # Local development only. Render uses its configured Gunicorn command.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
