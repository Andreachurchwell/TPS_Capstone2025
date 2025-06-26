import os
import csv
from datetime import datetime


# Define the data folder path relative to this file
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def save_current_weather_to_csv(data):
    filename = os.path.join(DATA_DIR, "current_weather.csv")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        data.get("name", ""),  # City
        now_str,               # Date & time
        data["main"].get("temp", ""),
        data["main"].get("humidity", ""),
        data["wind"].get("speed", ""),
        data["clouds"].get("all", ""),
        data.get("visibility", ""),
        data["weather"][0].get("description", "")
    ]

    header = ["City", "Datetime", "Temp(F)", "Humidity(%)", "Wind Speed(mph)", "Cloudiness(%)", "Visibility(m)", "Description"]

    write_header = not os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)




def save_forecast_to_csv(data):
    filename = os.path.join(DATA_DIR, "forecast.csv")

    header = ["City", "DateTime", "Temp(F)", "Description"]
    city = data.get("city", {}).get("name", "")

    write_header = not os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        for item in data.get("list", []):
            dt_txt = item.get("dt_txt", "")
            temp = item.get("main", {}).get("temp", "")
            desc = item.get("weather", [{}])[0].get("description", "")
            writer.writerow([city, dt_txt, temp, desc])
