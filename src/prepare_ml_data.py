import pandas as pd
import os

def prepare_data():
    try:
        # 1. Load the history you've been building
        df = pd.read_csv("data/latest_air_quality.csv")
        
        # 2. Convert the 'timestamp' text into real Date objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 3. Create 'Features' (Numbers the AI can understand)
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

        # 4. Save this 'Clean' data for the ML model
        output_path = "data/ml_ready_data.csv"
        df.to_csv(output_path, index=False)
        
        print("--- Feature Engineering Complete ---")
        print(f"New features created: Hour, Day of Week, Weekend Flag")
        print(df.head()) # Let's see the new columns!

    except Exception as e:
        print(f"Error preparing data: {e}")

if __name__ == "__main__":
    prepare_data()