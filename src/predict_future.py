import joblib
import pandas as pd
from datetime import datetime, timedelta

def predict_next_hour():
    # 1. Load the trained brain
    model = joblib.load('models/urban_pulse_model.pkl')
    
    # 2. Get the timing for "One Hour from Now"
    now = datetime.now()
    next_hour_time = now + timedelta(hours=1)
    
    hour = next_hour_time.hour
    day_of_week = next_hour_time.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0
    
    # 3. Format the data for the model
    input_data = pd.DataFrame([[hour, day_of_week, is_weekend]], 
                              columns=['hour', 'day_of_week', 'is_weekend'])
    
    # 4. Make the prediction
    prediction = model.predict(input_data)[0]
    
    print("--- URBAN PULSE AI PREDICTION ---")
    print(f"Current Time: {now.strftime('%I:%M %p')}")
    print(f"Predicting for: {next_hour_time.strftime('%I:%M %p')}")
    print(f"Predicted PM2.5 Level: {prediction:.2f} µg/m³")
    
    if prediction > 50:
        print("Warning: The AI predicts high pollution. Wear a mask! 😷")
    else:
        print("The AI predicts the air will be relatively clear. 🌳")

if __name__ == "__main__":
    predict_next_hour()