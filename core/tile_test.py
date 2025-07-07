# import tkinter as tk
# from tkintermapview import TkinterMapView
# import customtkinter as ctk
# import os
# from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("OPENWEATHER_API_KEY")



# # Available OpenWeather layers
# LAYER_OPTIONS = {
#     "OpenStreetMap (Default)": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
#     "Temperature": f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Precipitation": f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Clouds": f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Wind": f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Pressure": f"https://tile.openweathermap.org/map/pressure_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
# }

# def main():
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("blue")

#     root = ctk.CTk()
#     root.title("OpenWeather Tile Layer Test")
#     root.geometry("900x700")

#     # Map widget
#     map_widget = TkinterMapView(root, width=800, height=550, corner_radius=10)
#     map_widget.pack(pady=(20, 10))

#     map_widget.set_position(35.17, -88.59)  # Selmer, TN
#     map_widget.set_zoom(7)

#     # Dropdown to switch tile layer
#     def on_layer_change(selected):
#         tile_url = LAYER_OPTIONS[selected]
#         map_widget.set_tile_server(tile_url, max_zoom=19)

#     tile_dropdown = ctk.CTkOptionMenu(
#         root,
#         values=list(LAYER_OPTIONS.keys()),
#         command=on_layer_change,
#         width=300
#     )
#     tile_dropdown.set("OpenStreetMap (Default)")
#     tile_dropdown.pack(pady=(0, 20))

#     # Set default tile
#     map_widget.set_tile_server(LAYER_OPTIONS["OpenStreetMap (Default)"])

#     root.mainloop()

# if __name__ == "__main__":
#     main()



import tkinter as tk
from tkintermapview import TkinterMapView
import customtkinter as ctk
import os
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define all the available OpenWeather tile layers
LAYER_OPTIONS = {
    "OpenStreetMap (Default)": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
    "Temperature": f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Precipitation": f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Clouds": f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Wind": f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Pressure": f"https://tile.openweathermap.org/map/pressure_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
}

def main():
    # Basic CustomTkinter setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("OpenWeather Tile Layer Test")
    root.geometry("900x700")

    # --- Map Widget ---
    map_widget = TkinterMapView(root, width=800, height=550, corner_radius=10)
    map_widget.pack(pady=(20, 10))

    # Set initial map position and zoom
    map_widget.set_position(35.17, -88.59)  # Selmer, TN
    map_widget.set_zoom(7)

    # --- Dropdown to switch map tile layers ---
    def on_layer_change(selected):
        tile_url = LAYER_OPTIONS[selected]
        map_widget.set_tile_server(tile_url, max_zoom=19)

    tile_dropdown = ctk.CTkOptionMenu(
        root,
        values=list(LAYER_OPTIONS.keys()),
        command=on_layer_change,
        width=300
    )
    tile_dropdown.set("OpenStreetMap (Default)")  # Set default
    tile_dropdown.pack(pady=(0, 20))

    # Set initial tile server
    map_widget.set_tile_server(LAYER_OPTIONS["OpenStreetMap (Default)"])

    root.mainloop()

if __name__ == "__main__":
    main()
