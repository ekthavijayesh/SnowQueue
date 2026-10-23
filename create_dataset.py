from pathlib import Path
import numpy as np
import pandas as pd

# Reproducible synthetic data
rng = np.random.default_rng(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

rides = {
    "Family Snow Slide": {"capacity": 20, "cycle": 4.0},
    "Kids Snow Slide": {"capacity": 12, "cycle": 3.0},
    "Tube Ride": {"capacity": 16, "cycle": 5.0},
    "Sleigh Ride": {"capacity": 10, "cycle": 4.5},
    "Hanging Bridge": {"capacity": 8, "cycle": 2.5},
    "Kiddy Ride": {"capacity": 12, "cycle": 3.5},
}

rows = []

# 300 days x 6 attractions = 1,800 records
for day in range(300):
    day_type = "Weekend" if day % 7 in (5, 6) else "Weekday"
    attendance = int(
        rng.integers(150, 451) if day_type == "Weekend"
        else rng.integers(60, 251)
    )

    weather = rng.choice(
        ["Sunny", "Cloudy", "Rainy"],
        p=[0.35, 0.45, 0.20]
    )

    temperature = round(float(rng.uniform(24, 34)), 1)

    for ride_name, details in rides.items():
        hour = int(rng.integers(10, 22))
        is_peak = int(
            hour in (12, 13, 16, 17, 18, 19, 20)
            or day_type == "Weekend"
        )

        queue_length = int(max(
            0,
            rng.poisson(
                8
                + attendance * 0.12
                + is_peak * 12
                + (5 if weather == "Rainy" else 0)
            )
        ))

        capacity = details["capacity"]
        cycle = details["cycle"]

        # Approximate service rate and queue waiting time
        people_served_per_hour = capacity * (60 / cycle)
        effective_service = max(1, people_served_per_hour * 0.65)

        wait_time = (
            queue_length / effective_service * 60
            + rng.normal(2, 2)
        )
        wait_time = round(float(np.clip(wait_time, 0, 180)), 1)

        rows.append({
            "ride_name": ride_name,
            "hour": hour,
            "day_type": day_type,
            "weather": weather,
            "queue_length": queue_length,
            "ride_capacity": capacity,
            "ride_cycle_minutes": cycle,
            "park_attendance": attendance,
            "temperature_c": temperature,
            "is_peak_hour": is_peak,
            "wait_time_minutes": wait_time,
        })

df = pd.DataFrame(rows)
output_path = DATA_DIR / "queue_waiting_time.csv"
df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print("Saved to:", output_path)
print("Dataset shape:", df.shape)
print("\nRide names:")
print(sorted(df["ride_name"].unique()))
print("\nFirst 5 rows:")
print(df.head().to_string(index=False))
print("\nIMPORTANT: This is synthetic prototype data,")
print("not actual operational data from Snow Fantasy.")
