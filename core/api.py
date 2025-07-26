
import os
import requests
from dotenv import load_dotenv

# Load API key securely from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

print("[DEBUG] API key loaded successfully")


# ----------------------------------------
# Fetch current weather by city name
# ----------------------------------------
def fetch_current_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch current weather for {city}: {e}")
        return None


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
