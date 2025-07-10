import requests
import json
from dotenv import load_dotenv 
import os 

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
url = "https://api.openweathermap.org/data/2.5/forecast/daily"
params = {
    "q": "Selmer",         # You can change to any city
    "cnt": 16,             # Request up to 16 days
    "appid": API_KEY,  
    "units": "imperial"
}

response = requests.get(url, params=params)

try:
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Error parsing JSON:", e)