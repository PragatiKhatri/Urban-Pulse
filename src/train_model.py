import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib # This is to save our 'Brain' once it's trained

def train_urban_pulse():
    # 1. Load the ML-ready data
    df = pd.read_csv("data/ml_ready_data.csv")
    
    # --- NEW CLEANING STEP ---
    # This removes any rows where the pollution value is empty (NaN)
    initial_count = len(df)
    df = df.dropna(subset=['value'])
    final_count = len(df)
    
    if initial_count > final_count:
        print(f"Cleaned up {initial_count - final_count} empty rows.")
    # -------------------------

    # 2. Define what we use to guess (X) and what we want to predict (y)
    X = df[['hour', 'day_of_week', 'is_weekend']]
    y = df['value']
    
    # ... rest of your code ...

    
    # 3. Split data: 80% for learning, 20% for a "final exam"
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize the Random Forest (The Brain)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    print("Training the Urban Pulse AI... 🧠")
    model.fit(X_train, y_train)
    # After model.fit(X_train, y_train)
    importances = model.feature_importances_
    for i, feature in enumerate(['Hour', 'Day', 'Weekend']):
        print(f"{feature} Importance: {importances[i]:.2f}")
    
    # 5. Check how smart it is
    predictions = model.predict(X_test)
    error = mean_absolute_error(y_test, predictions)
    
    print(f"Training Complete! Average error: {error:.2f} µg/m³")
    
    # 6. Save the model to a file so we can use it later
    joblib.dump(model, 'models/urban_pulse_model.pkl')
    print("Model saved in 'models/' folder!")

if __name__ == "__main__":
    train_urban_pulse()