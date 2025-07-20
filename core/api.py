# import os  # handles file paths and env variables
# import requests  # http requests from OpenWeather
# from dotenv import load_dotenv  # loads my API key


# from geopy.geocoders import Nominatim
# # This is where I handle all my API requests to OpenWeather. I store the API key securely in a .env file, and 
# # then I have separate functions for getting current weather, forecast, extended forecast, and air quality. I use requests to fetch the data,
# # and I wrap the air quality call in a try/except to catch errors


# # Load API key from .env file
# load_dotenv()
# API_KEY = os.getenv("OPENWEATHER_API_KEY")
# print("[DEBUG] Loaded API_KEY:", API_KEY)

# # FETCHING CURRENT WEATHER BY THE CITIES NAME

# def fetch_current_weather(city):
#     try:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
#         response = requests.get(url, timeout=10)
#         # if response.status_code == 200:
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         # print(f"Error fetching weather: {response.status_code}")
#         print(f'XX request failed: {e}')
#         return None


# #FETCHING CURRENT WEATHER BY LATITUDE AND LONGITUDE (MORE ACCURATE THAN CITY NAME)

# def fetch_current_weather_by_coords(lat, lon):
#     url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching weather by coordinates: {response.status_code}")
#         return None


# # FETCHING 5-DAY FORECAST IN 3-HOUR INCREMENTS FOR A CITY
# # This gives more detailed trends (like temp changes throughout each day), not just daily summaries.
# def fetch_forecast(city):
#     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching forecast: {response.status_code}")
#         return None


# # Extended Forecast by City (deprecated endpoint)

# # def fetch_extended_forecast(city, days=7):
# #     url = (
# #         f"https://api.openweathermap.org/data/2.5/forecast/daily?"
# #         f"q={city}&cnt={days}&units=imperial&appid={API_KEY}"
# #     )
# #     return requests.get(url).json()

# # # Fetching air quality

# # def fetch_air_quality(lat, lon):
# #     api_key = os.getenv("OPENWEATHER_API_KEY")
# #     url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

# #     try:
# #         response = requests.get(url)
# #         response.raise_for_status()
# #         return response.json()
# #     except Exception as e:
# #         print("[ERROR] Failed to fetch air quality:", e)
# #         return None


# # def fetch_extended_forecast(city, days=7):
# #     print(f"[DEBUG] Making extended forecast API call for {city} ({days} days)")
    
# #     try:
# #         # Convert city name to lat/lon using geopy
# #         geolocator = Nominatim(user_agent="volunteer_weather_app")
# #         location = geolocator.geocode(city)

# #         if not location:
# #             print("[DEBUG] Geocoding failed")
# #             return None

# #         lat, lon = location.latitude, location.longitude

# #         url = "https://api.openweathermap.org/data/2.5/forecast/daily"
# #         params = {
# #             "lat": lat,
# #             "lon": lon,
# #             "cnt": days,
# #             "units": "imperial",
# #             "appid": API_KEY
# #         }

# #         response = requests.get(url, params=params, timeout=20)
# #         print(f"[DEBUG] Status Code: {response.status_code}")
# #         response.raise_for_status()
# #         return response.json()

# #     except requests.exceptions.RequestException as e:
# #         print(f"[DEBUG] Request failed: {e}")
# #         return None



# def fetch_extended_forecast(*args):
#     try:
#         if len(args) == 2 and isinstance(args[0], str):
#             # Case: (city_name, days)
#             city, days = args
#             print(f"[DEBUG] Making extended forecast API call for {city} ({days} days)")
#             geolocator = Nominatim(user_agent="volunteer_weather_app")
#             location = geolocator.geocode(city)

#             if not location:
#                 print("[DEBUG] Geocoding failed")
#                 return None

#             lat, lon = location.latitude, location.longitude

#         elif len(args) == 3:
#             # Case: (lat, lon, days)
#             lat, lon, days = args
#             print(f"[DEBUG] Making extended forecast API call for coordinates ({lat}, {lon}) ({days} days)")

#         else:
#             print("[DEBUG] Invalid arguments passed to fetch_extended_forecast()")
#             return None

#         url = "https://api.openweathermap.org/data/2.5/forecast/daily"
#         params = {
#             "lat": lat,
#             "lon": lon,
#             "cnt": days,
#             "units": "imperial",
#             "appid": API_KEY
#         }

#         response = requests.get(url, params=params, timeout=10)
#         print(f"[DEBUG] Status Code: {response.status_code}")
#         response.raise_for_status()
#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f'[DEBUG] Request failed: {e}')
#         return None







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
