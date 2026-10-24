# ❄️ SnowQueue – Snow Fantasy, HiLITE Mall, Kozhikode

### A Machine Learning-Based Queue Waiting-Time Estimation System for Snow Fantasy

**SnowQueue** is a machine-learning-powered web application developed as an MCA project to estimate queue waiting times for rides and activities at Snow Fantasy, HiLITE Mall, Kozhikode, Kerala. The application combines a trained regression model with a Flask backend and a responsive web interface to demonstrate how machine learning can be used for queue waiting-time estimation.

🌐 **Live Demo:** [https://snowqueue.onrender.com](https://snowqueue.onrender.com)

💻 **GitHub Repository:** [QueueWise-Amusement-Park](https://github.com/ekthavijayesh/QueueWise-Amusement-Park)

> **Disclaimer:** SnowQueue is an independent educational prototype. It is not an official application of Snow Fantasy or HiLITE Mall. Predictions are generated using synthetic educational data and do not represent live queue measurements or validated real-world waiting times.

---

## 📌 Project Overview

Snow Fantasy offers a snow-themed recreational experience at HiLITE Mall in Kozhikode, Kerala. During busy periods, waiting in queues can affect how visitors plan their activities.

SnowQueue explores how machine learning can estimate waiting times based on input features such as ride selection, hour of the day, day type, weather conditions, queue length, ride capacity, ride cycle duration, park attendance, and temperature.

Users enter the requested details through a web interface, and the trained model generates an estimated waiting time.

The project demonstrates an end-to-end machine-learning workflow, including dataset generation, exploratory data analysis, model training, model evaluation, web application development, and online deployment.

## 🎯 Project Objectives

- Develop a machine-learning-based waiting-time estimation system.
- Explore factors that may influence queue waiting times.
- Train and evaluate a regression model using a prepared dataset.
- Build an interactive web application using Flask, HTML, CSS, and JavaScript.
- Display estimated waiting times through a user-friendly interface.
- Deploy the application online for demonstration and educational purposes.

## ✨ Key Features

- ❄️ **SnowQueue branding:** A winter-inspired interface with an ice-blue and white theme.
- 🎯 **Waiting-time estimation:** Predicts an estimated waiting time using a trained regression model.
- 🎢 **Ride-specific inputs:** Allows users to select a ride or activity and enter queue-related details.
- 🕒 **Time-based features:** Considers the hour of the day and peak-hour information.
- 🌦️ **Environmental inputs:** Includes weather and temperature as model features.
- 📊 **Queue information:** Uses queue length, ride capacity, cycle duration, and park attendance.
- ⚡ **Interactive frontend:** Uses JavaScript to validate inputs and display prediction results.
- 🐍 **Flask backend:** Processes prediction requests and communicates with the trained model.
- 📈 **Exploratory data analysis:** Includes visualizations for investigating patterns in the dataset.
- 📱 **Responsive interface:** Designed to adapt to desktop and mobile screens.
- ☁️ **Online deployment:** Hosted on Render.

## 🌐 Live Application

Try SnowQueue online:

### 👉 [https://snowqueue.onrender.com](https://snowqueue.onrender.com)

### How to use the application

1. Open the SnowQueue website.
2. Select a ride or activity.
3. Enter the required queue, time, and environmental details.
4. Click the prediction button.
5. View the estimated waiting time and its descriptive category.

**Note:** The live application may take a little time to load after a period of inactivity because it uses a free hosting service. The predictions are experimental estimates and should not be treated as actual Snow Fantasy queue information.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web framework and prediction API |
| Pandas | Data processing and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine-learning algorithms and evaluation |
| Joblib | Saving and loading the trained model |
| HTML5 | Frontend structure |
| CSS3 | Styling, responsive design, and animations |
| JavaScript | Form validation and API communication |
| Matplotlib | Exploratory data visualizations |
| Git | Version control |
| GitHub | Source-code hosting |
| Git LFS | Version control for large files, where configured |
| Gunicorn | Production WSGI server |
| Render | Cloud deployment platform |

## 📂 Project Structure

```text
QueueWise-Amusement-Park/
│
├── data/
│   └── queue_waiting_time.csv
│
├── models/
│   ├── model_metadata.json
│   └── queue_wait_model.joblib
│
├── reports/
│   ├── figures/
│   └── model_comparison.csv
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
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

*This structure represents the project's intended organization. Optional reports and metadata files may differ depending on which files are present in the repository.*

### Important files

- `app.py` — Flask application used as the production entry point on Render.
- `server.py` — Alternative Flask application script for local development, if required by its configuration.
- `generate_dataset.py` — Script for generating the synthetic queue dataset.
- `eda.py` — Script for exploratory data analysis.
- `train_model.py` — Script for training and evaluating machine-learning models.
- `data/queue_waiting_time.csv` — Dataset used by the project.
- `models/queue_wait_model.joblib` — Saved trained model.
- `templates/index.html` — Main web interface.
- `static/style.css` — Styling and responsive layout.
- `static/script.js` — Frontend validation and prediction requests.
- `requirements.txt` — Python dependencies.

## ⚙️ Installation and Local Setup

Follow these steps to run SnowQueue on your local computer.

### 1. Prerequisites

Install the following:

- Python
- Git
- Visual Studio Code or another code editor

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

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, follow your normal Python environment setup instructions rather than changing system-wide security settings unnecessarily.

### 5. Install the dependencies

```powershell
python -m pip install -r requirements.txt
```

### 6. Verify the model and dataset

Make sure the trained model exists at:

```text
models/queue_wait_model.joblib
```

If the application requires the dataset during startup, also ensure that this file exists:

```text
data/queue_waiting_time.csv
```

If the model is managed using Git LFS, install Git LFS and make sure the actual model file has been downloaded rather than a small pointer file.

### 7. Run the Flask application

For the production application configured through `app.py`, run:

```powershell
python app.py
```

Open the following address in your browser:

**http://127.0.0.1:5000**

If you choose to run `server.py` instead, check its configuration and required input formats first. The deployed Render service is configured to use `app.py`.

## 🧠 Machine-Learning Approach

SnowQueue uses a supervised regression approach to estimate queue waiting times.

Regression is appropriate for this task because the target value is a numerical quantity: the estimated waiting time in minutes.

### Input features

The project's model uses the following features:

| Feature | Description |
|---|---|
| `ride_name` | Selected ride or activity |
| `hour` | Hour of the day |
| `day_type` | Weekday or weekend |
| `weather` | Weather condition |
| `queue_length` | Number of people represented by the queue input |
| `ride_capacity` | Ride capacity input |
| `ride_cycle_minutes` | Duration of a ride cycle in minutes |
| `park_attendance` | Park attendance input |
| `temperature_c` | Temperature in Celsius |
| `is_peak_hour` | Indicator derived from the hour |

The exact input types, permitted values, and feature ordering must match the saved model and the backend implementation.

### Machine-learning workflow

```text
Synthetic Dataset Generation
             ↓
Data Preparation
             ↓
Exploratory Data Analysis
             ↓
Feature Preparation
             ↓
Model Training
             ↓
Model Evaluation
             ↓
Save the Trained Model
             ↓
Flask Web Application
             ↓
User Inputs
             ↓
Estimated Waiting Time
```

### Model evaluation

The project's recorded evaluation results are:

| Evaluation metric | Recorded value |
|---|---:|
| Mean Absolute Error (MAE) | 6.566 |
| Root Mean Squared Error (RMSE) | 9.18 |
| R² Score | 0.9652 |

**Interpretation**

- **MAE:** Measures the average absolute difference between predicted and actual target values.
- **RMSE:** Measures prediction error while giving greater weight to larger errors.
- **R² Score:** Measures how much variation in the target values is explained by the model on the evaluated dataset.

These are the project's recorded results on synthetic educational data. They do not establish that the model will achieve equivalent performance on real Snow Fantasy queues. The results depend on the dataset, its generation process, and the evaluation methodology.

## 📊 Exploratory Data Analysis

Exploratory data analysis helps investigate the generated dataset before model training.

The project includes visualizations intended to examine:

- Distribution of waiting times.
- Average waiting time by ride.
- Waiting times across different hours.
- Differences in waiting times across input conditions.
- Model performance comparisons.

These visualizations support the study of patterns in the synthetic data. They should not be interpreted as verified measurements of actual Snow Fantasy operations.

## 🔌 How the Web Application Works

SnowQueue connects a browser-based frontend to a Python backend.

1. The user opens the website.
2. The user enters ride and queue information.
3. JavaScript validates the form and sends the input to the Flask `/predict` endpoint.
4. Flask checks the input values and prepares the model features.
5. The saved regression model produces an estimate.
6. Flask returns the result as JSON.
7. JavaScript displays the estimated waiting time on the webpage.

The model is loaded by the backend, so it does not need to be retrained for each prediction request.

## 🚀 Deployment on Render

SnowQueue is deployed using Render.

### Deployment configuration

| Setting | Configuration |
|---|---|
| Hosting platform | Render |
| Runtime | Python 3 |
| Production entry point | `app.py` |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### Deployment workflow

1. Commit and push the latest changes to GitHub.
2. Open the SnowQueue service in the Render dashboard.
3. Allow automatic deployment or manually deploy the latest commit.
4. Check the deployment logs for errors.
5. Open the public URL and test the prediction form.

**Live URL:** [https://snowqueue.onrender.com](https://snowqueue.onrender.com)

The website may take some time to start after inactivity on a free hosting plan.

## ⚠️ Limitations

- The dataset is synthetic and intended for educational purposes.
- SnowQueue does not retrieve live queue data from Snow Fantasy.
- Predicted waiting times are estimates and may differ from actual conditions.
- Recorded evaluation metrics do not guarantee real-world prediction accuracy.
- The model has not been established as a validated operational forecasting system for Snow Fantasy.
- Reliable real-world use would require authorized data collection, representative observations, independent validation, monitoring, and maintenance.
- The project is not officially affiliated with or endorsed by Snow Fantasy or HiLITE Mall.

## 🔮 Future Improvements

Potential future enhancements include:

- Integrating authorized real-time queue data, if an appropriate data source becomes available.
- Collecting and validating real waiting-time observations.
- Testing the model on independent, representative datasets.
- Comparing additional regression algorithms and tuning hyperparameters.
- Improving feature engineering and error analysis.
- Displaying prediction uncertainty when supported by a suitable statistical method.
- Adding automated tests for input validation and prediction endpoints.
- Improving accessibility and mobile usability.
- Monitoring application health and deployment errors.

## 🎓 Learning Outcomes

This project provides practical experience in:

- Understanding supervised machine learning and regression.
- Preparing structured datasets for modelling.
- Performing exploratory data analysis.
- Training and evaluating regression models.
- Saving and loading trained models with Joblib.
- Building REST-style prediction endpoints with Flask.
- Connecting HTML, CSS, and JavaScript to a Python backend.
- Managing project files using Git and GitHub.
- Deploying a Python web application using Render.

## 👩‍💻 Author

**Ektha M**  
MCA Student | Machine Learning Learner

GitHub: [@ekthavijayesh](https://github.com/ekthavijayesh)

## 📄 Disclaimer

SnowQueue is an independent educational project developed to demonstrate machine learning and web application development in the context of queue waiting-time estimation for Snow Fantasy at HiLITE Mall, Kozhikode.

It is not an official Snow Fantasy or HiLITE Mall application. All predictions are experimental estimates based on synthetic data and should not be relied upon for actual queue planning.


**Built as an MCA learning project with Python, machine learning, Flask, HTML, CSS, and JavaScript.**
