
import os
import requests
from dotenv import load_dotenv
from loguru import logger
import pandas as pd
import csv
from datetime import datetime
# Load API key securely from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

print("[DEBUG] API key loaded successfully")


# ----------------------------------------
# Fetch current weather by city name
# ----------------------------------------
# def fetch_current_weather(city):
#     try:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"[ERROR] Failed to fetch current weather for {city}: {e}")
#         # return None
#                 # Optional fallback: try to load from backup CSV
#         fallback = load_last_saved_weather(city)
#         if fallback:
#             print(f"[INFO] Showing last saved data for {city}")
#         return fallback
def fetch_current_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
        response = requests.get(url, timeout=10)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Return the actual error JSON if available (like {"cod": "404"})
            try:
                error_json = response.json()
                print(f"[ERROR] HTTP error with JSON: {error_json}")
                return error_json
            except Exception:
                print("[ERROR] Failed to parse error JSON.")
                return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch current weather for {city}: {e}")
        fallback = load_last_saved_weather(city)
        if fallback:
            print(f"[INFO] Showing last saved data for {city}")
        return fallback

# ----------------------------------------
# Fetch current weather by coordinates
# ----------------------------------------
def fetch_current_weather_by_coords(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch current weather by coordinates: {e}")
        return None


# ----------------------------------------
# 5-day forecast (3-hour increments) by city name
# ----------------------------------------
def fetch_forecast(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch 5-day forecast for {city}: {e}")
        return None


# ----------------------------------------
# Extended daily forecast (7/10/14/16-day) by coordinates
# ----------------------------------------
def fetch_extended_forecast(lat, lon, days=7):
    try:
        print(f"[DEBUG] Fetching {days}-day forecast for coordinates: ({lat}, {lon})")
        url = "https://api.openweathermap.org/data/2.5/forecast/daily"
        params = {
            "lat": lat,
            "lon": lon,
            "cnt": days,
            "units": "imperial",
            "appid": API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG] Status Code: {response.status_code}")
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch extended forecast: {e}")
        return None


# ----------------------------------------
# Air quality by coordinates
# ----------------------------------------
def fetch_air_quality(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch air quality: {e}")
        return None



def load_last_saved_weather(city):
    try:
        df = pd.read_csv("data/current_weather.csv")  # Adjust this path if needed
        df = df[df["city"].str.lower() == city.lower()]  # Match the city name, case-insensitive

        if df.empty:
            print(f"[INFO] No backup weather data found for {city}")
            return None

        # Get the most recent row for that city
        latest = df.sort_values("timestamp", ascending=False).iloc[0]

        print(f"[INFO] Loaded fallback data for {city} from {latest['timestamp']}")

        # Return a fake API-style dictionary
        return {
            "name": latest["city"],
            "main": {
                "temp": latest["temperature"],
                "humidity": latest["humidity"],
                "pressure": latest["pressure"]
            },
            "weather": [{
                "description": latest["description"],
                "icon": latest["icon"]
            }],
            "wind": {
                "speed": latest["wind_speed"]
            }
        }

    except Exception as e:
        print(f"[ERROR] Could not load fallback weather data: {e}")
        return None
    

def save_current_weather_to_csv(data):
    try:
        with open("data/current_weather.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                data["name"],
                data["main"]["temp"],
                data["main"]["humidity"],
                data["main"]["pressure"],
                data["weather"][0]["description"],
                data["weather"][0]["icon"],
                data["wind"]["speed"],
                datetime.now().isoformat()
            ])
    except Exception as e:
        print(f"[ERROR] Failed to save current weather to CSV: {e}")