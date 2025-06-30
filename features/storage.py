import os
import csv
from datetime import datetime


# Define the data folder path relative to this file
# sets up consistent place to store data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# makes sure folder exists(creates if not)
os.makedirs(DATA_DIR, exist_ok=True)
# save current weather to csv file
def save_current_weather_to_csv(data):
    # file path for current weather
    filename = os.path.join(DATA_DIR, "current_weather.csv")
# gets current date/time for the log
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# creates one row of data to write
    row = [
        data.get("name", ""),  # City
        now_str,               # Date & time
        data["main"].get("temp", ""),#temp
        data["main"].get("humidity", ""),#humidity %
        data["wind"].get("speed", ""),#wind speed
        data["clouds"].get("all", ""),#cloudiness %
        data.get("visibility", ""),#visiility
        data["weather"][0].get("description", "")#weather desc
    ]
# column headers for csv file
    header = ["City", "Datetime", "Temp(F)", "Humidity(%)", "Wind Speed(mph)", "Cloudiness(%)", "Visibility(m)", "Description"]
# ck if i need to write header (only if it dont exist)
    write_header = not os.path.exists(filename)
# open file and append row
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)


# save forecast data to seperate csv file

def save_forecast_to_csv(data):
    # filepath for forecast data
    filename = os.path.join(DATA_DIR, "forecast.csv")
# column headers
    header = ["City", "DateTime", "Temp(F)", "Description"]
    # gets city name from data safely
    city = data.get("city", {}).get("name", "")
    # ck if header needs to be written
    write_header = not os.path.exists(filename)
    # open fle and write each forecast entry
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        for item in data.get("list", []):
            dt_txt = item.get("dt_txt", "")#forecast datetime
            temp = item.get("main", {}).get("temp", "")#forecast temp
            desc = item.get("weather", [{}])[0].get("description", "")#forecast desc
            writer.writerow([city, dt_txt, temp, desc])
