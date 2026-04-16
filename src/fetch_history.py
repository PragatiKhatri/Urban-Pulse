import requests
import pandas as pd
from dotenv import load_dotenv
import os

# 1. Load the secret key from your .env file
load_dotenv()
API_KEY = os.getenv('OPENAQ_API_KEY')

def get_historical_data():
    # Location 8118 is New Delhi. Sensor 23534 is specifically PM2.5.
    sensor_id = 23534
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
    
    # FIX: Correct dictionary format for headers
    headers = {"X-API-Key": API_KEY}
    
    params = {"limit": 500}

    print("Traveling back in time to fetch Delhi history...")
    
    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            history_list = []
            
            for entry in data['results']:
                history_list.append({
                    "timestamp": entry['period']['datetimeFrom']['local'],
                    "parameter": "pm25",
                    "value": entry['value'],
                    "unit": "µg/m³"
                })
            
            df = pd.DataFrame(history_list)
            # This overwrites the small file with 500 real rows
            df.to_csv("data/latest_air_quality.csv", index=False)
            print(f"Done! Successfully pulled {len(df)} real historical data points.")
        else:
            print(f"Failed! Error: {response.status_code}")
            print("Check if your API Key is correct in the .env file.")

    except Exception as e:
        print(f"A connection error occurred: {e}")

if __name__ == "__main__":
    get_historical_data()