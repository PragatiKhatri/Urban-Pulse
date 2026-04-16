# 🌬️ Urban Pulse: AI-Powered Air Quality Predictor (Delhi)

**Urban Pulse** is a machine learning-driven application designed to predict $PM_{2.5}$ concentration levels in New Delhi. By leveraging real-time sensor data and historical trends, the system provides a 1-hour forward forecast to help citizens make informed health decisions.

---

## 🚀 Live Demo
[Insert your Streamlit Cloud Link Here After Deployment]

---

## 📌 Project Overview
Air pollution in New Delhi follows a highly volatile but cyclical pattern. This project moves beyond static datasets to interact with **live air quality sensors**. 

### Key Features:
* **Real-time Ingestion:** Connects to the **OpenAQ API** to fetch live data from Delhi-based sensors.
* **Automated Pipeline:** A full end-to-end flow from data fetching $\rightarrow$ cleaning $\rightarrow$ feature engineering $\rightarrow$ prediction.
* **Interactive Dashboard:** A Streamlit-based UI that visualizes 24-hour trends and displays instant health alerts.

---

## 🧠 Machine Learning Details

### The Model
I implemented a **Random Forest Regressor** to handle the non-linear nature of urban pollution. The model was trained on 500+ historical hourly records.

### Performance & Metrics
* **Mean Absolute Error (MAE):** 62.93 µg/m³
* **Feature Importance:**
    * **Hour of Day (65%):** Proved to be the strongest predictor of pollution spikes.
    * **Day of Week (31%):** Accounts for weekday traffic vs. weekend variations.
    * **Is Weekend (4%):** Shows that in Delhi, pollution levels remain significant even on weekends.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Libraries:** `scikit-learn`, `pandas`, `plotly`, `joblib`, `requests`
* **UI Framework:** Streamlit
* **Data Source:** OpenAQ Platform

---

## 📂 Project Structure
```text
UrbanPulse_ML/
├── data/                # Historical and ML-ready CSV files
├── models/              # Trained .pkl model files
├── src/
│   ├── fetch_history.py # Bulk data collection
│   ├── prepare_ml_data.py # Feature engineering logic
│   ├── train_model.py   # Model training & evaluation
│   └── predict_future.py# CLI prediction script
├── app.py               # Streamlit Dashboard (Main Entry Point)
└── requirements.txt     # Dependency list for deployment