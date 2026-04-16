import pandas as pd
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")

def check_delhi_air():
    # Location 8118 is a station in Delhi
    url = "https://api.openaq.org/v3/locations/8118/sensors"
    
    # Use an equals sign (=) here
    headers = {
        "X-API-Key": API_KEY
    }

    print("Connecting to the Urban Pulse...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("--- DATA RECEIVED ---")
            data = response.json()
            
            # 1. Create a list to hold our clean data
            clean_list = []
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for sensor in data['results']:
                if sensor.get('latest'):
                    # 2. Collect the details
                    entry = {
                        "timestamp": current_time,
                        "location": "New Delhi",  # Added this
                        "sensor_id": sensor['id'], # Added this
                        "parameter": sensor['parameter']['name'],
                        "value": sensor['latest']['value'],
                        "unit": sensor['parameter']['units']
                    }
                    clean_list.append(entry)
            
            # 3. Use Pandas to save it
            df = pd.DataFrame(clean_list)
            # This saves the file into your 'data' folder
            # Check if the file already exists
            file_path = "data/latest_air_quality.csv"
            file_exists = os.path.isfile(file_path)

            # Save the data: 
            # 'a' means APPEND (add to the end)
            # header=not file_exists means only write the column names the first time
            df.to_csv(file_path, mode='a', index=False, header=not file_exists)
            
            print(f"Added new data to {file_path}. The history is growing!")
            
            print("Successfully saved latest data to data/latest_air_quality.csv!")
            print(df) # This shows the table in your terminal

        elif response.status_code == 401:
            print("--- STOP ---")
            print("API Key not working. Check your email verification.")
        else:
            print(f"Error code: {response.status_code}")
            
    except Exception as e:
        print(f"Something went wrong: {e}")

# Added the missing colon (:) here
if __name__ == "__main__":
    check_delhi_air()