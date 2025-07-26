import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  
# Replace with Brett's actual API key
API_KEY = os.getenv("WEATHERBIT_API_KEY")

if not API_KEY:
    print("[ERROR] API key not found. Make sure WEATHERBIT_API_KEY is in your .env file.")
else:
    print("[DEBUG] API key loaded successfully")

    
LAT = 35.1701
LON = -88.5923

def generate_month_ranges(start_date, end_date):
    ranges = []
    current = start_date
    while current < end_date:
        next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        end = min(next_month - timedelta(days=1), end_date)
        ranges.append((current.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        current = next_month
    return ranges

start = datetime(2024, 7, 1)
end = datetime(2025, 6, 30)
month_ranges = generate_month_ranges(start, end)

all_data = []

for start_date, end_date in month_ranges:
    print(f"[INFO] Fetching {start_date} to {end_date}")
    url = "https://api.weatherbit.io/v2.0/history/daily"
    params = {
        "lat": LAT,
        "lon": LON,
        "start_date": start_date,
        "end_date": end_date,
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])
        all_data.extend(data)
    except Exception as e:
        print(f"[ERROR] Failed for {start_date} - {end_date}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Keep only needed columns
columns_needed = ["datetime", "max_wind_spd", "precip", "max_temp", "min_temp"]
df = df[columns_needed].copy()

# Rename and clean
df.rename(columns={"datetime": "date"}, inplace=True)
df["city"] = "Selmer"

# Reorder columns
df = df[["date", "city", "max_wind_spd", "precip", "max_temp", "min_temp"]]

# Save cleaned CSV
df.to_csv("cleaned_weather_data_selmer.csv", index=False)
print("[DONE] Saved clean file as cleaned_weather_data_selmer.csv")