


# import tkinter as tk
# from tkintermapview import TkinterMapView
# import customtkinter as ctk
# import os
# from dotenv import load_dotenv

# # Load the API key from .env
# load_dotenv()
# API_KEY = os.getenv("OPENWEATHER_API_KEY")

# # Define all the available OpenWeather tile layers
# LAYER_OPTIONS = {
#     "OpenStreetMap (Default)": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
#     "Temperature": f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Precipitation": f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Clouds": f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Wind": f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#     "Pressure": f"https://tile.openweathermap.org/map/pressure_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
# }

# def main():
#     # Basic CustomTkinter setup
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("blue")

#     root = ctk.CTk()
#     root.title("OpenWeather Tile Layer Test")
#     root.geometry("900x700")

#     # --- Map Widget ---
#     map_widget = TkinterMapView(root, width=800, height=550, corner_radius=10)
#     map_widget.pack(pady=(20, 10))

#     # Set initial map position and zoom
#     map_widget.set_position(35.17, -88.59)  # Selmer, TN
#     map_widget.set_zoom(7)

#     # --- Dropdown to switch map tile layers ---
#     def on_layer_change(selected):
#         tile_url = LAYER_OPTIONS[selected]
#         map_widget.set_tile_server(tile_url, max_zoom=19)

#     tile_dropdown = ctk.CTkOptionMenu(
#         root,
#         values=list(LAYER_OPTIONS.keys()),
#         command=on_layer_change,
#         width=300
#     )
#     tile_dropdown.set("OpenStreetMap (Default)")  # Set default
#     tile_dropdown.pack(pady=(0, 20))

#     # Set initial tile server
#     map_widget.set_tile_server(LAYER_OPTIONS["OpenStreetMap (Default)"])

#     root.mainloop()

# if __name__ == "__main__":
#     main()



import customtkinter as ctk
import folium
import webbrowser
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Weather tile overlays
WEATHER_TILES = {
    "Temperature": f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Precipitation": f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Clouds": f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Wind": f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
    "Pressure": f"https://tile.openweathermap.org/map/pressure_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
}

def create_folium_map(city, weather_tile_url):
    geolocator = Nominatim(user_agent="folium_tile_viewer")
    location = geolocator.geocode(city)

    if not location:
        print("City not found.")
        return

    lat, lon = location.latitude, location.longitude

    m = folium.Map(location=[lat, lon], zoom_start=7)

    # Add base map
    folium.TileLayer("OpenStreetMap").add_to(m)

    # Add weather overlay
    folium.TileLayer(
        tiles=weather_tile_url,
        attr="OpenWeatherMap",
        name="Weather Overlay",
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

    # Add a marker for the city
    folium.Marker(location=[lat, lon], popup=city).add_to(m)

    folium.LayerControl().add_to(m)

    filepath = "folium_map.html"
    m.save(filepath)
    webbrowser.open(filepath)

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Folium Weather Overlay Map")
    root.geometry("450x200")

    # --- Entry for City Name ---
    city_label = ctk.CTkLabel(root, text="Enter City:")
    city_label.pack(pady=(10, 5))

    city_entry = ctk.CTkEntry(root, width=300)
    city_entry.pack()

    # --- Dropdown for Weather Tile Type ---
    tile_label = ctk.CTkLabel(root, text="Select Weather Tile:")
    tile_label.pack(pady=(10, 5))

    selected_tile = ctk.StringVar(value="Temperature")

    tile_dropdown = ctk.CTkOptionMenu(
        root,
        values=list(WEATHER_TILES.keys()),
        variable=selected_tile,
        width=300
    )
    tile_dropdown.pack()

    # --- Button to Show Map ---
    def show_map():
        city = city_entry.get().strip()
        tile_type = selected_tile.get()
        if city and tile_type:
            weather_tile_url = WEATHER_TILES[tile_type]
            create_folium_map(city, weather_tile_url)

    show_button = ctk.CTkButton(root, text="Show Map", command=show_map)
    show_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()