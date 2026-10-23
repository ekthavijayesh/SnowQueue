# 🎢 QueueWise – Amusement Park Queue Waiting Time Prediction

**QueueWise** is a machine learning web application that predicts the estimated waiting time for amusement park rides. It uses historical queue data and a trained machine learning model to help visitors estimate waiting times and make better decisions when choosing rides.

## 📌 Project Overview

Waiting in long queues is a common problem at amusement parks. QueueWise aims to estimate ride waiting times using machine learning and present predictions through a simple, interactive web interface.

The project includes data generation, exploratory data analysis, model training, and a Flask-based web application.

## ✨ Features

- 🎯 Predict estimated ride waiting times using machine learning
- 🌐 Interactive web interface built with HTML, CSS, and JavaScript
- 🐍 Flask backend for handling prediction requests
- 📊 Exploratory data analysis and visualizations
- 🤖 Trained Extra Trees regression model
- 📁 Dataset and model evaluation reports
- 🔄 Scripts for generating data and training the model

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Flask** – Web application backend
- **Pandas** – Data processing
- **Scikit-learn** – Machine learning model
- **Joblib** – Saving and loading the trained model
- **HTML, CSS, JavaScript** – Frontend development
- **Matplotlib** – Data visualization
- **Git and GitHub** – Version control
- **Git LFS** – Managing large model files

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

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ekthavijayesh/QueueWise-Amusement-Park.git
cd QueueWise-Amusement-Park
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python server.py
```

Open the following address in your browser:

http://127.0.0.1:5000

**Note:** The trained model files must be available in the `models/` directory. Git LFS must successfully download the model files when cloning the repository.

## 🧠 Machine Learning Approach

QueueWise uses an **Extra Trees regression model** to estimate waiting times.

The workflow includes:

1. Generate or prepare the queue waiting-time dataset.
2. Explore the dataset and visualize patterns.
3. Train and evaluate machine learning models.
4. Save the selected model for prediction.
5. Load the trained model in the Flask application.
6. Display estimated waiting times through the web interface.

### Model Evaluation

The recorded evaluation results are:

| Metric | Value |
|---|---:|
| Mean Absolute Error (MAE) | 6.566 |
| Root Mean Squared Error (RMSE) | 9.18 |
| R² Score | 0.9652 |

These results are from the project's synthetic educational dataset. They should not be interpreted as evidence of equivalent accuracy with real amusement park data.

## 📊 Exploratory Data Analysis

The project includes visualizations for:

- Waiting-time distribution
- Average waiting time by ride
- Waiting time by hour
- Model performance comparison

These reports help explore patterns in the dataset and compare model performance.

## 🚀 Future Improvements

- Integrate real-time ride queue information
- Train and validate the model using real-world park data
- Add park and ride selection filters
- Improve prediction accuracy through feature engineering
- Deploy the application online
- Make the interface responsive for mobile devices

## ⚠️ Limitations

- The current dataset is synthetic and intended for educational purposes.
- Predictions may not reflect actual ride waiting times.
- Real-world deployment requires validation with reliable park
