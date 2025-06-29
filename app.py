# from core.api import fetch_current_weather, fetch_forecast

# def main():
#     city = input("Enter a city name: ")

#     # Current Weather
#     weather = fetch_current_weather(city)
#     if weather:
#         print(f"Current temperature in {city}: {weather['main']['temp']}°F")
#     else:
#         print("Could not get current weather data.")

#     # Forecast
#     forecast = fetch_forecast(city)
#     if forecast:
#         print("\n5-Day Forecast (every 3 hours):")
#         for item in forecast['list'][:5]:  # print first 5 data points only
#             dt = item['dt_txt']
#             temp = item['main']['temp']
#             description = item['weather'][0]['description']
#             print(f"{dt} | {temp}°F | {description}")
#     else:
#         print("Could not get forecast data.")


# if __name__ == "__main__":
#     main()

import tkinter as tk
from gui.main_window import MainWindow
# from gui.main_window2 import MainWindow2
# import subprocess

def main():
    root = tk.Tk()
    app = MainWindow(root)
    # app = MainWindow2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
