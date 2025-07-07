import os  # handles file paths and env variables
import requests  # http requests from OpenWeather
from dotenv import load_dotenv  # loads your API key

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ----------------------------
# 📍 Current Weather by City
# ----------------------------
def fetch_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather: {response.status_code}")
        return None

# ----------------------------
# 📍 Current Weather by Coordinates
# ----------------------------
def fetch_current_weather_by_coords(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather by coordinates: {response.status_code}")
        return None

# ----------------------------
# 📍 Forecast by City
# ----------------------------
def fetch_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching forecast: {response.status_code}")
        return None

# ----------------------------
# 📍 Extended Forecast by City (deprecated endpoint)
# ----------------------------
def fetch_extended_forecast(city, days=7):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast/daily?"
        f"q={city}&cnt={days}&units=imperial&appid={API_KEY}"
    )
    return requests.get(url).json()

# Fetching air quality
# ------------------------------
def fetch_air_quality(lat, lon):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("[ERROR] Failed to fetch air quality:", e)
        return None