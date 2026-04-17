import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# 1. Page Config
st.set_page_config(page_title="Urban Pulse Delhi", page_icon="🌬️")

st.title("🌬️ Urban Pulse: New Delhi Air Quality")
st.markdown("Real-time $PM_{2.5}$ predictions using Machine Learning.")

# 2. The Fail-Safe Loader
def load_or_train_model(df):
    model_path = 'models/urban_pulse_model.pkl'
    
    # Try to load the existing model
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            # Test it to ensure version compatibility
            test_data = pd.DataFrame([[0, 0, 0]], columns=['hour', 'day_of_week', 'is_weekend'])
            model.predict(test_data)
            return model
        else:
            raise FileNotFoundError
    except Exception:
        # If loading fails or version is wrong, train a fresh one on the server
        st.warning("🔄 Syncing model with cloud environment...")
        X = df[['hour', 'day_of_week', 'is_weekend']]
        y = df['value'] # Using the 'value' column from your CSV
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

@st.cache_resource
def load_assets():
    # Load the data first so we can use it to train if needed
    df = pd.read_csv('data/latest_air_quality.csv')
    # Ensure columns are named correctly for training
    df['timestamp'] = pd.to_datetime(df['date_local'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.weekday
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    model = load_or_train_model(df)
    return model, df

# Load assets
model, df = load_assets()

# 3. Sidebar - Current Stats
st.sidebar.header("Live Station Info")
st.sidebar.write("📍 Location: New Delhi")
st.sidebar.write(f"📊 Latest Reading: {df['value'].iloc[0]} µg/m³")

# 4. The Prediction Logic
st.subheader("Next Hour Forecast")
if st.button("Predict Future Air Quality"):
    next_hour = datetime.now() + timedelta(hours=1)
    # Prepare input for model
    input_df = pd.DataFrame([[next_hour.hour, next_hour.weekday(), 1 if next_hour.weekday() >= 5 else 0]], 
                            columns=['hour', 'day_of_week', 'is_weekend'])
    
    prediction = model.predict(input_df)[0]
    
    # Display Result
    col1, col2 = st.columns(2)
    col1.metric("Predicted PM2.5", f"{prediction:.2f} µg/m³")
    
    if prediction > 150: # Adjusting threshold for Delhi context
        st.error("⚠️ Hazardous levels predicted. Wear a mask!")
    elif prediction > 50:
        st.warning("😷 Moderate pollution. Limit outdoor time.")
    else:
        st.success("✅ Clear air predicted.")

# 5. The History Chart
st.subheader("Recent Pollution Trends")
fig = px.line(df.head(24), x='timestamp', y='value', title='Last 24 Hours PM2.5 Levels')
st.plotly_chart(fig)