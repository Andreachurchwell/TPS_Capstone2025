# # import requests
# # import os
# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv

# # load_dotenv()
# # API_KEY = os.getenv("OWM_API_KEY")
# # CITY = "Selmer"

# # def get_current_weather(city):
# #     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
# #     return requests.get(url).json()

# # def get_forecast(city):
# #     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
# #     return requests.get(url).json()

# # def get_air_pollution(lat, lon):
# #     url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
# #     return requests.get(url).json()

# # def get_climate_forecast(city):
# #     url = f"http://pro.openweathermap.org/data/2.1/climate/forecast?q={city}&appid={API_KEY}"
# #     return requests.get(url).json()

# # def get_historical_weather(lat, lon):
# #     # Only one year back supported in Student Plan
# #     dt = int((datetime.now() - timedelta(days=365)).timestamp())
# #     url = f"http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={dt}&cnt=24&appid={API_KEY}"
# #     return requests.get(url).json()

# # def test_all():
# #     current = get_current_weather(CITY)
# #     print("\n=== CURRENT WEATHER ===")
# #     print(current)

# #     forecast = get_forecast(CITY)
# #     print("\n=== 5-DAY FORECAST ===")
# #     print(forecast)

# #     lat = current['coord']['lat']
# #     lon = current['coord']['lon']

# #     pollution = get_air_pollution(lat, lon)
# #     print("\n=== AIR POLLUTION ===")
# #     print(pollution)

# #     try:
# #         climate = get_climate_forecast(CITY)
# #         print("\n=== CLIMATE FORECAST (30 DAY) ===")
# #         print(climate)
# #     except Exception as e:
# #         print("\nClimate forecast failed (this may need pro endpoint):", e)

# #     try:
# #         history = get_historical_weather(lat, lon)
# #         print("\n=== HISTORICAL WEATHER ===")
# #         print(history)
# #     except Exception as e:
# #         print("\nHistorical weather failed:", e)

# # if __name__ == "__main__":
# #     test_all()


# # import requests
# # import os
# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv
# # import pytz

# # load_dotenv()
# # API_KEY = os.getenv("OWM_API_KEY")
# # CITY = "Selmer"

# # def get_current_weather(city):
# #     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
# #     return requests.get(url).json()

# # def get_forecast(city):
# #     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
# #     return requests.get(url).json()

# # def get_air_pollution(lat, lon):
# #     url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
# #     return requests.get(url).json()

# # def get_historical_weather(lat, lon):
# #     dt = int((datetime.now() - timedelta(days=365)).timestamp())
# #     url = f"http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={dt}&cnt=24&appid={API_KEY}"
# #     return requests.get(url).json()

# # def get_tornado_window(lat, lon):
# #     # April 3, 2025 at 12:34 AM CDT (America/Chicago)
# #     dt_local = datetime(2025, 4, 3, 0, 34)
# #     tz = pytz.timezone("America/Chicago")
# #     dt_utc = tz.localize(dt_local).astimezone(pytz.utc)
# #     unix_ts = int(dt_utc.timestamp())

# #     # 24 hours before and after
# #     url = (
# #         f"http://history.openweathermap.org/data/2.5/history/city?"
# #         f"lat={lat}&lon={lon}&type=hour"
# #         f"&start={unix_ts - 86400}"  # 24 hours before
# #         f"&cnt=48&appid={API_KEY}"
# #     )
# #     return requests.get(url).json()

# # def test_all():
# #     current = get_current_weather(CITY)
# #     print("\n=== CURRENT WEATHER ===")
# #     print(current)

# #     forecast = get_forecast(CITY)
# #     print("\n=== 5-DAY FORECAST ===")
# #     print(forecast)

# #     lat = current['coord']['lat']
# #     lon = current['coord']['lon']

# #     pollution = get_air_pollution(lat, lon)
# #     print("\n=== AIR POLLUTION ===")
# #     print(pollution)

# #     try:
# #         history = get_historical_weather(lat, lon)
# #         print("\n=== HISTORICAL WEATHER (1 YEAR AGO) ===")
# #         print(history)
# #     except Exception as e:
# #         print("\nHistorical weather failed:", e)

# #     try:
# #         tornado = get_tornado_window(lat, lon)
# #         print("\n=== TORNADO PERIOD WEATHER (Apr 2–4, 2025) ===")

# #         highest = {"wind": 0, "time": "", "weather": ""}

# #         for hour in tornado.get('list', []):
# #             timestamp = datetime.utcfromtimestamp(hour['dt']).strftime('%Y-%m-%d %H:%M:%S')
# #             wind = hour['wind']['speed']
# #             weather = hour['weather'][0]['main']

# #             if wind > highest["wind"]:
# #                 highest["wind"] = wind
# #                 highest["time"] = timestamp
# #                 highest["weather"] = weather

# #             print(f"{timestamp} UTC | {weather} | Wind: {wind} m/s")

# #         mph = highest["wind"] * 2.237  # Convert to mph

# #         print("\n🌪️ HIGHEST WIND DURING TORNADO WINDOW:")
# #         print(f"{highest['time']} UTC | {highest['weather']} | {highest['wind']} m/s ({mph:.1f} mph)")

# #     except Exception as e:
# #         print("\nTornado data failed:", e)

# # if __name__ == "__main__":
# #     test_all()



# import tkinter as tk
# from tkintermapview import TkinterMapView



# # ----------- Setup root window -----------
# root = tk.Tk()
# root.geometry("800x600")
# root.title("OpenWeather Map Tile Tester")

# # ----------- Map widget -----------
# map_widget = TkinterMapView(root, width=800, height=550, corner_radius=0)
# map_widget.pack()

# # Center map on Selmer, TN
# map_widget.set_position(35.1701, -88.5923)
# map_widget.set_zoom(6)

# # Set default OpenStreetMap layer
# map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

# # ----------- Layer change function -----------
# def set_layer(layer_name):
#     print(f"Switching to layer: {layer_name}")
#     tile_url = f"https://tile.openweathermap.org/map/{layer_name}/{{z}}/{{x}}/{{y}}.png?appid={OPENWEATHER_API_KEY}"
#     map_widget.set_tile_server(tile_url)

#     # Force tile reload by nudging zoom
#     map_widget.set_zoom(map_widget.zoom + 0.1)
#     map_widget.set_zoom(map_widget.zoom - 0.1)

# # ----------- Reset to OpenStreetMap -----------
# def reset_to_osm():
#     print("Switching to OpenStreetMap")
#     map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
#     map_widget.set_zoom(map_widget.zoom + 0.1)
#     map_widget.set_zoom(map_widget.zoom - 0.1)

# # ----------- Buttons -----------
# btn_frame = tk.Frame(root, bg="#2E2E2E")
# btn_frame.pack(pady=5)

# layers = ["radar", "clouds_new", "precipitation_new", "temp_new", "wind_new"]

# for layer in layers:
#     btn = tk.Button(
#         btn_frame,
#         text=layer.replace("_new", "").capitalize(),
#         command=lambda l=layer: set_layer(l),
#         bg="#444",
#         fg="white",
#         padx=10,
#         relief="flat"
#     )
#     btn.pack(side="left", padx=5)

# # Add reset button
# reset_btn = tk.Button(btn_frame, text="Reset Map", command=reset_to_osm, bg="#777", fg="white")
# reset_btn.pack(side="left", padx=5)

# # ----------- Run the app -----------
# root.mainloop()

