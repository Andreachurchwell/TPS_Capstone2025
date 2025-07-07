import tkinter as tk
from tkinter import ttk
from datetime import datetime
from core.api import fetch_current_weather, fetch_forecast, fetch_extended_forecast
from core.icons import get_icon_image, get_detail_icon
from features.storage import save_current_weather_to_csv, save_forecast_to_csv

from features.dark_light_mode import ThemeToggle 

from features.map_feature import MapFeature


import subprocess
import sys
import os
from tkinter import messagebox

# for logo
from PIL import Image, ImageTk


from gui.forecast_popups import show_forecast_popup, process_forecast_data,process_extended_forecast_data

from features.radar_launcher import launch_radar_map

from core.weather_database import save_forecast_to_db

from features.custom_buttons import create_button, create_forecast_segmented_button
import customtkinter as ctk
from features.autocomplete import AutocompleteEntry
from core.api import fetch_current_weather_by_coords

from core.api import fetch_air_quality


class MainWindow:
    def __init__(self, root):

        # makes the main app window
        self.root = root
        self.root.title("AChurchwell-TPS2025-Capstone")
        self.root.geometry("1000x900") # sets my window size
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.current_theme = "dark"    # makes it start it dark mode

        # self.city_var = tk.StringVar(value='Selmer') # makes selmer my original city
        self.city_var = tk.StringVar() # makes selmer my original city

        # --- Centered Search Row ---
        self.input_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_container.pack(pady=10)

        self.input_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.input_frame.pack(anchor='center')


        autocomplete_theme = {
            "bg": "#3A3A3A",         # fallback for dark
            "fg": "#EBE8E5",
            "highlight": "#FF8C00",
            "border": "#FF8C00"
        }

        self.city_entry = AutocompleteEntry(
            master=self.input_frame,
            width=240,
            font=("Segoe UI", 12),
            theme_colors=autocomplete_theme
        )
        self.city_entry.pack(side="left", padx=(0, 5))

        self.search_button = create_button(
            parent=self.input_frame,
            text="Search",
            command=self.get_weather,
            theme=self.current_theme
        )
        self.search_button.pack(side="left", padx=(5, 0))


                # Temperature Unit Switch (F / C)
        self.unit_switch = ctk.CTkSwitch(
            self.input_frame,
            text="°F / °C",
            command=self.update_weather_units,
            onvalue=True,
            offvalue=False,
            progress_color="orange",
            fg_color="#444444",
            button_color="white",
            button_hover_color="gray"
)
        self.unit_switch.pack(side="left", padx=(10, 0)) 
        self.use_fahrenheit = not self.unit_switch.get()
        # --- Logo Section (circular + centered under search bar) ---


        logo_path = os.path.join("assets", "icons", "vw.png")
        logo_raw = Image.open(logo_path).resize((60, 60))
        self.logo_img = ImageTk.PhotoImage(logo_raw)


        # Display logo centered under the input frame
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg="#2E2E2E")
        self.logo_label.pack(pady=(10, 0))



        # Theme toggle button that links to the apply theme function
        self.theme_toggle_container = tk.Frame(self.root, bg="#2E2E2E")
        self.theme_toggle_container.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

        self.theme_toggle = ThemeToggle(
            parent=self.theme_toggle_container,
            toggle_callback=self.apply_theme,
            current_theme=self.current_theme,
            size=(24, 24)
        )
        self.theme_toggle.button.pack()

        # --- Main Weather Card Frame ---
        self.weather_card = ctk.CTkFrame(
            self.root,
            fg_color="#3A3A3A",
            corner_radius=12,
            border_width=3,
            border_color="#FFA040"  # Orange border around full card
        )
        self.weather_card.pack(pady=(20,10), padx=12)

        # Top row container
        self.card_row = ctk.CTkFrame(self.weather_card, fg_color="transparent")
        self.card_row.pack(padx=10, pady=(10,15))

                # --- Left: City + Icon + Temp
        self.left_section = ctk.CTkFrame(
            self.card_row,
            fg_color="#3a3a3a",
            corner_radius=8,
            # border_width=1,
            # border_color="black",  # Soft border
            width=220
        )
        self.left_section.pack(side="left", padx=(0, 8), fill="y")

        self.city_label = ctk.CTkLabel(
            self.left_section,
            text="Selmer",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color="#FFA040"
        )
        self.city_label.pack(pady=(0, 10))

        self.icon_label = tk.Label(
            self.left_section,
            bg="#3a3a3a"
        )
        self.icon_label.pack(pady=(0, 10))

        self.temp_desc_label = ctk.CTkLabel(
            self.left_section,
            text="94°F, Very Heavy Rain",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color="white"
        )
        self.temp_desc_label.pack(pady=(0, 10))

        # --- Right: 3x3 Grid Weather Stats (Tic-Tac-Toe Style)
        self.right_section = ctk.CTkFrame(
            self.card_row,
            fg_color="#3a3a3a",
            corner_radius=12,
            border_width=1,
            border_color="#444444"  # Matches left
        )
        self.right_section.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        # Make a dict to hold labels for easy updating later
        self.detail_labels = {}

        grid_keys = [
            "Humidity", "Wind", "Cloudiness",
            "Feels Like", "Pressure", "Visibility",
            "Gusts", "Rain", "Sunrise/Sunset"
        ]

        for idx, key in enumerate(grid_keys):
            row = idx // 3
            col = idx % 3
            label = ctk.CTkLabel(
                self.right_section,
                text=f"{get_detail_icon(key)} {key}: --",
                font=ctk.CTkFont("Segoe UI", 11, "bold"),
                text_color="white",
                anchor="w"
            )
            label.grid(
                row=row,
                column=col,
                sticky="w",
                padx=20,
                pady=10,
                ipady=6,
                ipadx=6
            )
            self.detail_labels[key] = label

        # Set column weight so they stretch evenly
        for i in range(3):
            self.right_section.grid_columnconfigure(i, weight=1)

        # Add map frame and map widget
        self.map_frame = ttk.Frame(self.root)
        self.map_frame.pack(pady=10)
        # makes map widget using custom mapfeature class
        self.map = MapFeature(self.map_frame)


                # ---- Map Tile Layer Dropdown ----
        tile_layers = {
            "OpenStreetMap": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Radar": f"https://tile.openweathermap.org/map/radar/{{z}}/{{x}}/{{y}}.png?appid={os.getenv('OPENWEATHER_API_KEY')}",
            "Clouds": f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={os.getenv('OPENWEATHER_API_KEY')}",
            "Precipitation": f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={os.getenv('OPENWEATHER_API_KEY')}",
            "Temperature": f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={os.getenv('OPENWEATHER_API_KEY')}",
            "Wind": f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={os.getenv('OPENWEATHER_API_KEY')}",
        }



        self.tile_layer_var = ctk.StringVar(value="OpenStreetMap")

        self.tile_dropdown = ctk.CTkOptionMenu(
            master=self.root,
            values=list(tile_layers.keys()),
            variable=self.tile_layer_var,
            command=lambda selection: self.change_map_layer(tile_layers[selection])
        )
        self.tile_dropdown.configure(
            width=200,
            height=32,
            fg_color="#444444",
            button_color="#555555",
            button_hover_color="orange",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 12)
        )
        self.tile_dropdown.pack(pady=5)

      


# leave this out for now bc i dont wanna show this!!!!! But ITS DEF GOING IN MY CAPSTONE SO DONOT DELETE ANDREA!!!!
        self.radar_button = create_button(
            parent=self.root,
            text="Live Radar",
            command=self.open_radar_map,
            theme=self.current_theme
        )
        self.radar_button.pack(pady=10)

                # creates fram for my forecast btns
        self.forecast_button_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.forecast_button_frame.pack(pady=5)



        self.forecast_label = ctk.CTkLabel(
            master=self.forecast_button_frame,
            text="Select Daily Forecast",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color="dark gray"
        )
        self.forecast_label.pack(pady=(5, 2))
        self.forecast_toggle = create_forecast_segmented_button(
            parent=self.forecast_button_frame,
            on_select_callback=self.handle_forecast_button_click,
            theme="dark"  # or "light"
        )
        self.forecast_toggle.pack(pady=10)



        self.setup_styles() # applies custom widget style

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handles graceful shutdown

        self.root.after(100, self.get_weather) # fetches weather for selmer(my default)





    def setup_styles(self):
        style = ttk.Style()
# style for main weather card
        style.configure("MainCard.TFrame", background="#3a3a3a", relief="flat", borderwidth=1)
# style for city name label thats big and bold
        style.configure("CityTitle.TLabel", background="#3a3a3a", foreground="#ffa040", font=("Segoe UI", 22, "bold"))
# style for temp and condition label
        style.configure("Condition.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 14,'bold'))
# style for all the detail labels
        style.configure("Detail.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10))


    def get_weather(self):
        # Check if the user selected a suggestion (has lat/lon)
        location = self.city_entry.selected_location

        if location:
            #  Use coordinates if selected from autocomplete
            lat = location["lat"]
            lon = location["lon"]
            weather = fetch_current_weather_by_coords(lat, lon)
            city_name = location.get("label", "Unknown")  # For debug or error messages
        else:
            #  User typed a city name manually
            city = self.city_entry.get().strip()
            if not city:
                city = "Selmer"  # Default fallback
            weather = fetch_current_weather(city)
            city_name = city  # For debug or error messages

        #  Debug print to check what city was used in the API response
        if weather:
            print("[DEBUG] Weather API response says city is:", weather.get("name"))
        else:
            print("[DEBUG] No weather data returned for:", city_name)

        # Error handling if city is invalid or API failed
        if not weather or "main" not in weather or "weather" not in weather:
            messagebox.showerror(
                "City Not Found",
                f"Oops! '{city_name}' doesn't seem to be a real city.\nDouble-check your spelling and try again."
            )
            self.city_entry.focus_set()
            return

        # Process valid weather data
        temp_k = weather["main"]["temp"]
        formatted_temp = self.format_temp(temp_k)
        description = weather["weather"][0]["description"].title()
        icon_code = weather["weather"][0]["icon"]

        self.city_label.configure(text=location.get("label", weather["name"]) if location else weather["name"])

        self.temp_desc_label.configure(text=f"{formatted_temp}, {description}")

        # Display weather icon
        icon_image = get_icon_image(icon_code)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image  # Keep a reference

        #  Update map to show new location
        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        self.map.update_location(lat, lon)

        #  Clear out old detail labels so they don't stack
        for label in self.detail_labels.values():
            label.destroy()
        self.detail_labels.clear()

        # ROW 0
        self.detail_labels["Humidity"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Humidity')} Humidity: {weather['main']['humidity']}%",
            style="Detail.TLabel"
        )
        self.detail_labels["Humidity"].grid(row=0, column=0, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        self.detail_labels["Wind"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Wind')} Wind: {weather['wind']['speed']} mph",
            style="Detail.TLabel"
        )
        self.detail_labels["Wind"].grid(row=0, column=1, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        self.detail_labels["Cloudiness"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Cloudiness')} Cloudiness: {weather['clouds']['all']}%",
            style="Detail.TLabel"
        )
        self.detail_labels["Cloudiness"].grid(row=0, column=2, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        # ROW 1
        feels_like = self.format_temp(weather["main"]["feels_like"])
        self.detail_labels["Feels Like"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Feels Like')} Feels Like: {feels_like}",
            style="Detail.TLabel"
        )
        self.detail_labels["Feels Like"].grid(row=1, column=0, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        self.detail_labels["Pressure"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Pressure')} Pressure: {weather['main']['pressure']} hPa",
            style="Detail.TLabel"
        )
        self.detail_labels["Pressure"].grid(row=1, column=1, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        self.detail_labels["Visibility"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Visibility')} Visibility: {weather.get('visibility', 0)/1000:.1f} km",
            style="Detail.TLabel"
        )
        self.detail_labels["Visibility"].grid(row=1, column=2, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        # ROW 2
        wind_gust = weather["wind"].get("gust")
        self.detail_labels["Wind Gust"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Gust')} Gusts: {wind_gust} mph" if wind_gust else "Gusts: N/A",
            style="Detail.TLabel"
        )
        self.detail_labels["Wind Gust"].grid(row=2, column=0, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        rain_1h = weather.get("rain", {}).get("1h", 0)
        self.detail_labels["Rain"] = ttk.Label(
            self.right_section,
            text=f"{get_detail_icon('Rain')} Rain (1h): {rain_1h} mm",
            style="Detail.TLabel"
        )
        self.detail_labels["Rain"].grid(row=2, column=1, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        sunrise_time = datetime.fromtimestamp(weather['sys']['sunrise']).strftime("%I:%M %p")
        sunset_time = datetime.fromtimestamp(weather['sys']['sunset']).strftime("%I:%M %p")
        sunrise_sunset_text = f"{get_detail_icon('Sunrise')} {sunrise_time} / {sunset_time}"

        self.detail_labels["Sunrise/Sunset"] = ttk.Label(
            self.right_section,
            text=sunrise_sunset_text,
            style="Detail.TLabel"
        )
        self.detail_labels["Sunrise/Sunset"].grid(row=2, column=2, sticky="w", padx=20, pady=10, ipady=6,ipadx=6)

        # Save the weather to CSV
        save_current_weather_to_csv(weather)

        # Clear the saved location
        self.city_entry.selected_location = None



    def open_radar_map(self):
        city = self.city_entry.get().strip().split(",")[0]
        if not city:
            self.show_custom_popup("Missing City", "Please enter a city before launching radar.")
            return

        launch_radar_map(city, self.show_custom_popup)

    def change_map_layer(self, tile_url):
        print(f"Switching map tiles to: {tile_url}")
        self.map.map_widget.set_tile_server(tile_url)
        self.map.map_widget.set_zoom(self.map.map_widget.zoom + 0.1)
        self.map.map_widget.set_zoom(self.map.map_widget.zoom - 0.1) 




    def apply_theme(self, theme_name):
        # store current theme
        self.current_theme = theme_name
        print(f"Theme switched to: {theme_name}")

        # inits ttk styling engine
        style = ttk.Style()

        if theme_name == "dark":
            bg_color = "#2E2E2E"     # window bg
            fg_color = "#EBE8E5"     # text color
            card_bg = "#3A3A3A"      # cards/input bg
            accent = "#FF8C00"       # orange accent for buttons
        else:
            bg_color = "#F9F6F3"     # light, soft background
            fg_color = "#222222"     # dark text
            card_bg = "#FFFFFF"      # white cards/input
            accent = "#FFA94D"       # soft orange accent

        # Set main window bg
        self.root.configure(bg=bg_color)

        # TTK styles
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TEntry", fieldbackground=card_bg, background=card_bg, foreground=fg_color)
        style.configure("TButton", background=card_bg, foreground=fg_color)

        style.configure("InputRow.TFrame", background=bg_color)

        # Map for button hover/active
        style.map("Accent.TButton",
                background=[("active", accent), ("!active", accent)],
                foreground=[("active", "white"), ("!active", "white")])


                # Update forecast button row background to match current theme
        if hasattr(self, 'forecast_button_frame'):
            self.forecast_button_frame.configure(bg=bg_color)


        

        # Manually update CustomTkinter widgets
        self.input_container.configure(fg_color="transparent")
        self.input_frame.configure(fg_color="transparent")

        try:
            if isinstance(self.city_entry, ctk.CTkEntry):
                self.city_entry.configure(
                    fg_color=card_bg,
                    text_color=fg_color,
                    placeholder_text_color="#AAAAAA" if theme_name == "light" else "#CCCCCC"
                )
            else:
                # fallback: standard tkinter Entry (like AutocompleteEntry)
                self.city_entry.entry.configure(
                    bg=card_bg,
                    fg=fg_color,
                    insertbackground=fg_color  # sets caret color
                )
        except Exception as e:
            self.city_entry.configure(bg=accent)
            print("City entry styling skipped due to:", e)




        self.search_button.configure(
            fg_color=accent,
            hover_color="#FFB866" if theme_name == "light" else "#FFA040",
            text_color="white" if theme_name == "dark" else fg_color
        )

        # Regular Tk widgets (logo + toggle container)
        self.theme_toggle_container.configure(bg=bg_color)
        self.logo_label.configure(bg=bg_color)

        # Map frame (ttk)
        self.map_frame.configure(style="TFrame")

        # Weather card (ttk)
        self.weather_card.configure(style="MainCard.TFrame")


    def handle_forecast_button_click(self, days):
        city = self.city_var.get().strip()
        if not city:
            city = 'Selmer'

        if days in [3, 5]:  # ← these use standard 3-hour forecast
            forecast = fetch_forecast(city)
            if not forecast or "list" not in forecast:
                self.show_custom_popup("Forecast Error", f"Could not retrieve forecast data for '{city}'.")
                return

            save_forecast_to_csv(forecast)
            forecast_summary = process_forecast_data(forecast, days)

        else:  # ← 7, 10, 16 use extended forecast
            forecast = fetch_extended_forecast(city, days)
            if not forecast or "list" not in forecast:
                self.show_custom_popup("Extended Forecast Error", f"Could not retrieve extended forecast for '{city}'.")
                return

            forecast_summary = process_extended_forecast_data(forecast, days)

        # Save to DB
        formatted_forecast = []
        for day in forecast_summary:
            if day["high"] == "--":
                continue
            formatted_forecast.append({
                "date": day["date"],
                "min_temp": day["low"],
                "max_temp": day["high"],
                "humidity": 55,
                "wind_speed": 5.2,
                "description": day["desc"],
                "icon_code": day["icon"]
            })
        save_forecast_to_db(city, formatted_forecast)

        while len(forecast_summary) < days:
            forecast_summary.append({
                "date": f"Day +{len(forecast_summary) + 1}",
                "high": "--", "low": "--",
                "desc": "Predicted Day", "icon": "01d"
            })

        show_forecast_popup(
            self.root,
            city,
            forecast_summary,
            days,
            theme=self.current_theme,
            format_temp_func=self.format_temp
        )


    
    def show_custom_popup(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#3A3A3A")
        popup.geometry("300x150")
        popup.resizable(False, False)

        label = tk.Label(
            popup,
            text=message,
            font=("Segoe UI", 10),
            fg="white",
            bg="#3A3A3A",
            wraplength=280,
            justify="center"
        )
        label.pack(pady=20, padx=10)

        close_button = tk.Button(
            popup,
            text="OK",
            command=popup.destroy,
            bg="#5a5a5a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            activebackground="#777777",
            activeforeground="white"
        )
        close_button.pack(pady=10)

        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)


    def format_temp(self, temp):
        try:
            temp = float(temp)  # Fixes the bug!
        except ValueError:
            return "N/A"

        if self.use_fahrenheit:
            return f"{round(temp)}°F"
        else:
            celsius = (temp - 32) * 5 / 9
            return f"{round(celsius)}°C"


    def update_weather_units(self):
        self.use_fahrenheit = not self.unit_switch.get()  # True = °F, False = °C
        self.get_weather()  # Optional: refresh weather display after toggling


    def on_close(self):
        try:
            self.map.destroy()
        except Exception as e:
            print("Map cleanup error:", e)

        self.root.after(100, self.root.destroy)  #Slight delay to avoid crashing background threads
        os._exit(0)







        

















