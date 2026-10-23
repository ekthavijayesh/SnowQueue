
from pathlib import Path

import numpy as np
import pandas as pd

# Save the dataset inside the project's data folder.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
n = 5000

rides = [
    "Roller Coaster",
    "Ferris Wheel",
    "Water Ride",
    "Drop Tower",
    "Carousel",
    "Haunted House",
]

ride_name = rng.choice(rides, n)
hour = rng.integers(9, 23, n)
day_type = rng.choice(["Weekday", "Weekend"], n, p=[0.55, 0.45])
weather = rng.choice(["Sunny", "Cloudy", "Rainy"], n, p=[0.55, 0.30, 0.15])
queue_length = rng.integers(0, 151, n)
ride_capacity = rng.choice([12, 16, 20, 24, 30, 36], n)
ride_cycle_minutes = rng.uniform(2, 8, n).round(1)
park_attendance = rng.integers(500, 12001, n)
temperature_c = rng.uniform(18, 40, n).round(1)
is_peak_hour = ((hour >= 12) & (hour <= 18)).astype(int)

# Simulated waiting time for educational model training.
ride_factor_map = {
    "Roller Coaster": 1.3,
    "Ferris Wheel": 0.8,
    "Water Ride": 1.1,
    "Drop Tower": 0.9,
    "Carousel": 0.6,
    "Haunted House": 1.0,
}
ride_factor = np.array([ride_factor_map[r] for r in ride_name])
weekend_factor = np.where(day_type == "Weekend", 1.25, 1.0)
weather_factor = np.where(weather == "Rainy", 0.65, 1.0)
peak_factor = np.where(is_peak_hour == 1, 1.2, 0.85)

wait_time_minutes = (
    queue_length * ride_cycle_minutes / ride_capacity
    * 3.2
    * ride_factor
    * weekend_factor
    * weather_factor
    * peak_factor
    + park_attendance / 1200
    + rng.normal(0, 3, n)
)
wait_time_minutes = np.clip(wait_time_minutes, 0, 180).round(1)

df = pd.DataFrame({
    "ride_name": ride_name,
    "hour": hour,
    "day_type": day_type,
    "weather": weather,
    "queue_length": queue_length,
    "ride_capacity": ride_capacity,
    "ride_cycle_minutes": ride_cycle_minutes,
    "park_attendance": park_attendance,
    "temperature_c": temperature_c,
    "is_peak_hour": is_peak_hour,
    "wait_time_minutes": wait_time_minutes,
})

output_path = DATA_DIR / "queue_waiting_time.csv"
df.to_csv(output_path, index=False)

print(f"Dataset created successfully: {output_path}")
print(f"Rows and columns: {df.shape}")
print(df.head())
