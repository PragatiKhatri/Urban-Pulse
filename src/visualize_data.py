import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_report():
    # 1. Load the data you fetched earlier
    try:
        df = pd.read_csv("data/latest_air_quality.csv")
        
        # 2. Check if we have enough data
        if len(df) < 1:
            print("The CSV is empty! Run fetch_data.py a few more times.")
            return

        # 3. Set the style
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        # 4. Create a Bar Chart showing the pollution value
        # We use a bar chart because right now you only have a few rows
        sns.barplot(x="timestamp", y="value", data=df, palette="Reds_d")

        # 5. Add a "Danger Line" at 15 (WHO Limit)
        plt.axhline(15, color='green', linestyle='--', label='WHO Safe Limit')

        # 6. Labels
        plt.title("Urban Pulse: Real-Time PM2.5 Levels in New Delhi")
        plt.xticks(rotation=45)
        plt.legend()

        # 7. Save the image
        plt.tight_layout()
        plt.savefig("data/air_quality_graph.png")
        print("Success! Your graph has been saved in the 'data' folder.")
        
    except FileNotFoundError:
        print("I can't find the CSV file. Did you run fetch_data.py yet?")

if __name__ == "__main__":
    create_report()