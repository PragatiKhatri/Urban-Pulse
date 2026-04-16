import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timedelta
import plotly.express as px # Great for interactive 

# 1. Page Config
st.set_page_config(page_title="Urban Pulse Delhi", page_icon="🌬️")

st.title("🌬️ Urban Pulse: New Delhi Air Quality")
st.markdown("Real-time $PM_{2.5}$ predictions using Machine Learning.")

# 2. Load the Model and Data
@st.cache_resource # This keeps the app fast
def load_assets():
    model = joblib.load('models/urban_pulse_model.pkl')
    df = pd.read_csv('data/latest_air_quality.csv')
    return model, df

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
    
    if prediction > 50:
        st.error("⚠️ Hazardous levels predicted. Wear a mask!")
    else:
        st.success("✅ Clear air predicted.")

# 5. The History Chart
st.subheader("Recent Pollution Trends")
df['timestamp'] = pd.to_datetime(df['timestamp'])
fig = px.line(df.head(24), x='timestamp', y='value', title='Last 24 Hours')
st.plotly_chart(fig)