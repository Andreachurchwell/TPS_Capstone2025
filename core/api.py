import os #handles file paths and env variables
import requests #http requests from openweather
from dotenv import load_dotenv #loads my api key


# Load API key from .env file (keeps sensitive info safe)
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_current_weather(city):
    # builds the url using city name, api key, and sets to fahreneheit
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
    # makes a get request to openweather
    response = requests.get(url)
    # if successful, returns python dict(json)
    if response.status_code == 200:
        return response.json()
    else:
        # if an error, prints error code and returns none
        print(f"Error fetching weather: {response.status_code}")
        return None


def fetch_forecast(city):
    # builds url to get 5 day in 3 hr intrvals
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
    # makes api call
    response = requests.get(url)
    # returns the parsed json if successful
    if response.status_code == 200:
        return response.json()
    else:
        # if theres an issue, logs it and returs none
        print(f"Error fetching forecast: {response.status_code}")
        return None
