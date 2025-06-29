import os
from dotenv import load_dotenv
import sys
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.api import fetch_current_weather, fetch_forecast

load_dotenv()  # Load API key

def test_fetch_current_weather_valid_city():
    result = fetch_current_weather("Selmer")
    assert result is not None
    assert "main" in result
    assert "weather" in result

def test_fetch_current_weather_invalid_city():
    result = fetch_current_weather("FAKECITY123")
    assert result is None

def test_fetch_forecast_valid_city():
    result = fetch_forecast("Selmer")
    assert result is not None
    assert "list" in result
    assert isinstance(result["list"], list)
    assert len(result["list"]) > 0

def test_fetch_forecast_invalid_city():
    result = fetch_forecast("FAKECITY123")
    assert result is None

if __name__ == "__main__":
    test_fetch_current_weather_valid_city()
    test_fetch_current_weather_invalid_city()
    test_fetch_forecast_valid_city()
    test_fetch_forecast_invalid_city()
    print("✅ All simple API tests passed.")
