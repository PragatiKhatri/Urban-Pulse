import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

st.title("🌬️ Urban Pulse: Delhi")

# 1. Load Data
df = pd.read_csv('data/latest_air_quality.csv')

# 2. Simple Training (Happens every time you open the app)
# This avoids ALL version errors because it uses the server's own version
X = pd.DataFrame({
    'hour': pd.to_datetime(df.iloc[:, 0]).dt.hour,
    'day': pd.to_datetime(df.iloc[:, 0]).dt.weekday
})
y = df['value']
model = RandomForestRegressor().fit(X, y)

# 3. Display
st.metric("Latest PM2.5", f"{y.iloc[0]} µg/m³")
if st.button("Predict"):
    st.write(f"Forecast: {model.predict([[12, 1]])[0]:.2f}")