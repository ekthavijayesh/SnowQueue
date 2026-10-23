
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "queue_waiting_time.csv"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("\n========== DATASET OVERVIEW ==========")
print("Dataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))

print("\n========== WAITING TIME BY RIDE ==========")
print(
    df.groupby("ride_name")["wait_time_minutes"]
    .agg(["mean", "median", "min", "max"])
    .round(2)
)

# 1. Distribution of waiting times
plt.figure(figsize=(9, 5))
plt.hist(df["wait_time_minutes"], bins=30, edgecolor="black")
plt.title("Distribution of Queue Waiting Times")
plt.xlabel("Waiting time (minutes)")
plt.ylabel("Number of observations")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "waiting_time_distribution.png")
plt.close()

# 2. Average waiting time for each ride
ride_wait = df.groupby("ride_name")["wait_time_minutes"].mean().sort_values()

plt.figure(figsize=(10, 5))
ride_wait.plot(kind="bar")
plt.title("Average Waiting Time by Ride")
plt.xlabel("Ride")
plt.ylabel("Average waiting time (minutes)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "average_wait_by_ride.png")
plt.close()

# 3. Waiting time by hour
hour_wait = df.groupby("hour")["wait_time_minutes"].mean()

plt.figure(figsize=(9, 5))
hour_wait.plot(marker="o")
plt.title("Average Waiting Time by Hour")
plt.xlabel("Hour of the day")
plt.ylabel("Average waiting time (minutes)")
plt.xticks(range(9, 23))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "waiting_time_by_hour.png")
plt.close()

print("\nEDA completed successfully!")
print("Charts saved in:", FIGURES_DIR)
