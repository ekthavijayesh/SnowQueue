# ❄️ SnowQueue – Amusement Park Queue Waiting-Time Estimator

**Estimate the wait. Plan the fun. Enjoy the snow.**

SnowQueue is a machine-learning-powered web application designed to estimate amusement park ride waiting times through a simple, interactive interface. Built as an MCA learning project, it combines a trained regression model with a Flask backend and a responsive frontend inspired by the winter experience of Snow Fantasy at HiLITE Mall, Kozhikode, Kerala.

> 🌐 **Live Demo:** https://snowqueue.onrender.com  
> 💻 **GitHub Repository:** https://github.com/ekthavijayesh/QueueWise-Amusement-Park

**Important:** SnowQueue is an independent educational prototype. It is not an official Snow Fantasy application. Predictions are based on synthetic data and are not live queue measurements or validated real-world forecasts.

---

## 📌 Project Overview

Waiting in long queues can affect how visitors plan their amusement park experience. SnowQueue explores how machine learning can estimate ride waiting times based on factors such as ride selection, time of day, day type, weather, queue length, ride capacity, ride cycle duration, park attendance, and temperature.

Users enter relevant information into a web form, and the trained model returns an estimated waiting time.

The project demonstrates an end-to-end machine-learning workflow, from dataset preparation and exploratory data analysis to model training, deployment, and interactive prediction.

## ✨ Features

- ❄️ **Winter-inspired interface** with an ice-blue and white visual theme.
- 🎯 **Waiting-time estimation** using a trained regression model.
- 🎢 **Ride-specific inputs** for estimating queue waiting times.
- 🕒 **Time and attendance factors** to explore their relationship with waiting times.
- 🌦️ **Weather and temperature inputs** for model-based estimates.
- ⚡ **Interactive prediction form** with JavaScript validation and result display.
- 🐍 **Flask backend** for processing requests and returning predictions.
- 📊 **Exploratory data analysis** to investigate waiting-time patterns.
- 🤖 **Saved machine-learning model** loaded for predictions without retraining on each request.
- 📱 **Responsive frontend** designed for desktop and mobile screens.
- ☁️ **Online deployment** using Render.

## 🌐 Live Application

Try the deployed application:

### 👉 https://snowqueue.onrender.com

Open the website, enter the requested ride and queue details, and submit the form to receive an estimated waiting time.

*Note: The free hosting service may take some time to start after a period of inactivity.*

## 🖥️ Application Preview

The application is designed around a clean, winter-inspired experience featuring:

- A SnowQueue-branded welcome section
- Ride and queue input fields
- A waiting-time prediction form
- An estimated result with a descriptive category
- A responsive layout and subtle snowfall effects

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web server and prediction API |
| Pandas | Dataset processing and feature preparation |
| NumPy | Numerical operations |
| Scikit-learn | Machine-learning model and preprocessing |
| Joblib | Saving and loading the trained model |
| HTML5 | Webpage structure |
| CSS3 | Styling, responsive layout, and animations |
| JavaScript | Form validation and API communication |
| Matplotlib | Exploratory data visualizations |
| Git and GitHub | Version control and source-code hosting |
| Git LFS | Large-file version control, where configured |
| Render | Web application hosting |
| Gunicorn | Production WSGI server |

## 📂 Project Structure

```text
QueueWise-Amusement-Park/
├── data/
│   └── queue_waiting_time.csv
├── models/
│   ├── model_metadata.json
│   └── queue_wait_model.joblib
├── reports/
│   ├── figures/
│   └── model_comparison.csv
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── app.py
├── server.py
├── eda.py
├── generate_dataset.py
├── train_model.py
├── requirements.txt
├── .gitattributes
├── .gitignore
└── README.md
```

*The structure above reflects the project's existing layout. Some generated reports or metadata files may be optional, depending on the files committed to the repository.*

## ⚙️ Installation and Local Setup

Follow these steps to run SnowQueue on your computer.

### 1. Prerequisites

Install:

- Python
- Git
- A code editor such as Visual Studio Code

### 2. Clone the repository

Open PowerShell or a terminal and run:

```powershell
git clone https://github.com/ekthavijayesh/QueueWise-Amusement-Park.git
cd QueueWise-Amusement-Park
```

### 3. Create a virtual environment

```powershell
python -m venv venv
```

### 4. Activate the environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Verify the required files

Ensure that the trained model is available at:

```text
models/queue_wait_model.joblib
```

The dataset should be available at:

```text
data/queue_waiting_time.csv
```

If the model is tracked using Git LFS, ensure Git LFS is installed and the actual model file has been downloaded rather than a small pointer file.

### 7. Run the application

For the local application configured through `app.py`:

```powershell
python app.py
```

Then open:

**http://127.0.0.1:5000**

> If you specifically use `server.py` for local development, follow that file's configuration instead. The deployed Render service uses `app.py` when configured with the start command below.

## 🚀 Deployment

SnowQueue is deployed on Render.

### Deployment configuration

| Setting | Value |
|---|---|
| Platform | Render |
| Runtime | Python 3 |
| Production entry point | `app.py` |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### Deployment workflow

1. Push the updated source code to GitHub.
2. Open the SnowQueue service in the Render dashboard.
3. Allow automatic deployment or manually deploy the latest commit.
4. Check the deployment logs for errors.
5. Open the live URL and test the prediction form.

**Live application:** https://snowqueue.onrender.com

## 🧠 Machine-Learning Approach

SnowQueue uses a trained regression model to estimate waiting times from structured input features.

### Input features

The model uses the following features, subject to the exact feature order expected by the saved model:

- Ride name
- Hour of the day
- Day type
- Weather condition
- Queue length
- Ride capacity
- Ride cycle duration
- Park attendance
- Temperature
- Peak-hour indicator

### Workflow

Dataset Preparation
        ↓
Exploratory Data Analysis
        ↓
Feature Preparation
        ↓
Model Training and Evaluation
        ↓
Save Trained Model
        ↓
Flask Web Application
        ↓
User Inputs
        ↓
Predicted Waiting Time


### Model evaluation

The project's recorded evaluation results are:

| Metric | Recorded value |
|---|---:|
| Mean Absolute Error (MAE) | 6.566 |
| Root Mean Squared Error (RMSE) | 9.18 |
| R² Score | 0.9652 |

These metrics are from the project's synthetic educational dataset and its recorded evaluation. They do not establish equivalent performance on real amusement park queues. Performance on new data may differ substantially.

## 📊 Exploratory Data Analysis

The project includes analysis and visualizations intended to explore:

- Distribution of waiting times
- Average waiting time by ride
- Waiting times across different hours
- Comparisons of candidate model performance

These analyses help examine patterns in the generated dataset and support experimentation with machine-learning models.

## 🔌 Application Workflow

1. The user opens the SnowQueue website.
2. The user enters the required ride, time, queue, and environmental details.
3. JavaScript validates the form and sends the input to the Flask backend.
4. Flask prepares the input features in the order expected by the saved model.
5. The model generates an estimated waiting time.
6. The application displays the estimate and an explanatory category.

## ⚠️ Limitations

- The dataset is synthetic and intended for educational purposes.
- The application does not access live Snow Fantasy queue systems.
- Predictions are estimates, not actual waiting times.
- Recorded evaluation metrics do not guarantee real-world accuracy.
- Real-world use would require permission to access reliable park data, validation, monitoring, and model updates.
- The application is not officially affiliated with or endorsed by Snow Fantasy or HiLITE Mall.

## 🔮 Future Improvements

- Integrate authorized, real-time queue information if available.
- Collect and validate real-world waiting-time data.
- Evaluate the model on independent, representative data.
- Compare additional regression algorithms and tune model parameters.
- Improve feature engineering and error analysis.
- Add clearer prediction confidence or uncertainty information where statistically justified.
- Expand accessibility and mobile usability testing.
- Add automated tests for API validation and prediction responses.
- Monitor deployment health and application errors.

## 🎓 Learning Outcomes

This project provides practical experience with:

- Understanding a supervised machine-learning regression problem
- Preparing structured datasets
- Performing exploratory data analysis
- Training and evaluating regression models
- Saving and loading models with Joblib
- Building a Flask prediction endpoint
- Connecting HTML, CSS, and JavaScript to a Python backend
- Using Git and GitHub for version control
- Deploying a Python application to a cloud hosting platform

## 👩‍💻 Author

**Ektha M**  
MCA Student | Machine Learning Learner

GitHub: https://github.com/ekthavijayesh


## 📄 Disclaimer

SnowQueue is an independent educational project created to demonstrate machine learning and web application development. It is not an official amusement park service. All predictions are experimental estimates based on synthetic data and should not be relied upon for actual queue planning.
