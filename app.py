
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="QueueWise | Waiting Time Predictor",
    page_icon="🎢",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "queue_wait_model.joblib"
DATA_PATH = BASE_DIR / "data" / "queue_waiting_time.csv"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F6F8F4;
    color: #24352D;
}
h1, h2, h3 {
    color: #24352D;
}
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #DCE5DC;
    padding: 18px;
    border-radius: 12px;
}
.stButton > button {
    background-color: #52796F;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #354F52;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL AND DATA ----------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

st.title("🎢 QueueWise")
st.subheader("Amusement Park Queue Waiting Time Predictor")
st.write(
    "Estimate how long visitors may wait for a ride based on "
    "queue conditions and operating factors."
)

if not MODEL_PATH.exists():
    st.error("Trained model not found. Run `python train_model.py` first.")
    st.stop()

if not DATA_PATH.exists():
    st.error("Dataset not found. Check the project's data folder.")
    st.stop()

model = load_model()
df = load_data()

st.info(
    "Demo version: predictions use a synthetic educational dataset. "
    "They are not validated forecasts for a real amusement park."
)

st.divider()

# ---------------- PREDICTION FORM ----------------
st.header("Predict Ride Waiting Time")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        ride_name = st.selectbox(
            "Select ride",
            sorted(df["ride_name"].unique()),
        )
        hour = st.slider("Hour of day", 9, 22, 14)
        day_type = st.selectbox(
            "Day type",
            ["Weekday", "Weekend"],
        )
        weather = st.selectbox(
            "Weather",
            ["Sunny", "Cloudy", "Rainy"],
        )

    with col2:
        queue_length = st.number_input(
            "People currently in queue",
            min_value=0,
            max_value=1000,
            value=50,
            step=1,
        )
        ride_capacity = st.selectbox(
            "People per ride cycle",
            [12, 16, 20, 24, 30, 36],
        )
        ride_cycle_minutes = st.slider(
            "Ride cycle duration (minutes)",
            2.0,
            8.0,
            4.0,
            step=0.5,
        )

    with col3:
        park_attendance = st.number_input(
            "Estimated total park attendance",
            min_value=0,
            max_value=100000,
            value=5000,
            step=100,
        )
        temperature_c = st.slider(
            "Temperature (°C)",
            10.0,
            45.0,
            28.0,
            step=0.5,
        )

    is_peak_hour = int(12 <= hour <= 18)

    submitted = st.form_submit_button(
        "Predict Waiting Time",
        use_container_width=True,
    )

if submitted:
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
        "is_peak_hour": is_peak_hour,
    }])

    prediction = float(model.predict(input_data)[0])
    prediction = max(0.0, prediction)

    st.divider()
    st.header("Prediction Result")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "Estimated waiting time",
            f"{prediction:.1f} minutes",
        )

    with metric_col2:
        st.metric(
            "Estimated waiting time",
            f"{prediction / 60:.2f} hours",
        )

    if prediction < 15:
        st.success("Short estimated wait")
    elif prediction < 45:
        st.warning("Moderate estimated wait")
    else:
        st.error("Long estimated wait")

    st.caption(
        "This is a model estimate based on simulated training data, "
        "not a verified live queue measurement."
    )

# ---------------- DATASET INSIGHTS ----------------
st.divider()
st.header("Dataset Insights")

col1, col2, col3 = st.columns(3)
col1.metric("Training dataset records", f"{len(df):,}")
col2.metric("Number of rides", df["ride_name"].nunique())
col3.metric(
    "Average simulated wait",
    f"{df['wait_time_minutes'].mean():.1f} min",
)

left, right = st.columns(2)

with left:
    st.subheader("Average wait by ride")
    average_wait = (
        df.groupby("ride_name")["wait_time_minutes"]
        .mean()
        .sort_values()
    )
    st.bar_chart(average_wait)

with right:
    st.subheader("Waiting time distribution")
    st.histogram if False else None
    st.bar_chart(
        df.groupby("hour")["wait_time_minutes"].mean()
    )
    st.caption("Average simulated waiting time by hour")

st.caption(
    "QueueWise • Educational machine-learning prototype"
)
