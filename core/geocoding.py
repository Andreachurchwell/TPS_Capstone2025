import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# def get_city_suggestions(query, limit=5):
#     if not query:
#         return []
#     print(f"[DEBUG] Searching for: {query}")
#     url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit={limit}&appid={API_KEY}"

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         suggestions = []
#         for city in data:
#             name = city.get("name", "")
#             state = city.get("state", "")
#             country = city.get("country", "")
#             display = f"{name}, {state}, {country}".strip(", ")
#             suggestions.append(display)

#         return suggestions

#     except Exception as e:
#         print("Error fetching city suggestions:", e)
#         return []


import requests
import os

def get_city_suggestions(query):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        suggestions = []
        for item in data:
            name = item.get("name", "")
            state = item.get("state", "")
            country = item.get("country", "")
            lat = item.get("lat")
            lon = item.get("lon")

            label = f"{name}, {state}, {country}" if state else f"{name}, {country}"
            value = f"{name},{state},{country}" if state else f"{name},{country}"

            suggestions.append({
                "label": label,
                "value": value,
                "lat": lat,
                "lon": lon
            })
        # print("[DEBUG] Suggestions from OpenWeather:", suggestions)
        return suggestions

    except Exception as e:
        print("Error fetching city suggestions:", e)
        return []