import tkinter as tk
from tkinter import ttk
from datetime import datetime
from core.api import fetch_current_weather, fetch_forecast, fetch_extended_forecast
from core.icons import get_icon_image, get_detail_icon
from features.storage import save_current_weather_to_csv, save_forecast_to_csv
from features.dark_light_mode import ThemeToggle 
from features.map_feature import MapFeature
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from gui.forecast_popups import show_forecast_popup, process_forecast_data,process_extended_forecast_data
from core.weather_database import save_forecast_to_db
from features.custom_buttons import create_button, create_forecast_segmented_button
from features.autocomplete import AutocompleteEntry
from core.api import fetch_current_weather_by_coords
from features.radar_launcher import launch_radar_map_by_coords, launch_radar_map_by_name
from features.temp_trend_chart import display_temperature_chart
import threading
from geopy.geocoders import Nominatim
from features.dark_light_mode import theme_colors
from datetime import datetime, timedelta
from team_7_Folder.team_dashboard import render_team_dashboard
from features.fonts import title_font, label_font,button_font,popup_font
import requests
from ml.predict_today_from_db import predict_max_temp



def get_local_time_from_offset(offset_seconds):
    utc_now = datetime.utcnow()
    local_time = utc_now + timedelta(seconds=offset_seconds)
    return local_time.strftime("%I:%M %p")




# MainWindow is the core GUI class that builds and runs the weather app
class MainWindow:
    def __init__(self, root):

        # makes the main app window
        self.root = root
        self.root.title("AChurchwell-TPS2025-Capstone")
        self.root.geometry("1000x900") # sets my window size
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.current_theme = "dark"    # makes it start it dark mode
        # --- Logo Section ---
        logo_path = os.path.join("assets", "icons", "vw.png")
        logo_raw = Image.open(logo_path).resize((40, 40))
        self.logo_img = ImageTk.PhotoImage(logo_raw)
        # --- Top-left logo ---
        self.logo_label = tk.Label(
            self.root,
            image=self.logo_img,
            bg="#2E2E2E"
        )
        self.logo_label.place(x=10, y=10)


    #   stores the city name from the input (used for forecast btns)
        self.city_var = tk.StringVar() # makes selmer my original city

    # top search row setup (input, search, unit toggle)
        self.input_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_container.pack(pady=10)

        self.input_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.input_frame.pack(anchor='center')

# autocomplete input for city search with dark styling
        autocomplete_theme = {
            "bg": "#3A3A3A",         # fallback for dark
            "fg": "#EBE8E5",
            "highlight": "#FF8C00",
            "border": "#FF8C00"
        }
        self.city_entry = AutocompleteEntry(
            master=self.input_frame,
            width=240,
            font=label_font,
            theme_colors=autocomplete_theme
        )
        self.city_entry.pack(side="left", padx=(0, 5))
    

# search btn triggers weather fetch
        self.search_button = create_button(
            parent=self.input_frame,
            text="Search",
            command=self.get_weather,
            theme=self.current_theme
        )
        self.search_button.pack(side="left", padx=(5, 0))
        try:
            self.city_entry.entry.bind("<Return>", lambda event: self.get_weather())
        except Exception as e:
            print("Binding failed:", e)

                # Temperature Unit Switch (F / C)
        self.unit_switch = ctk.CTkSwitch(
            self.input_frame,
            text="°F / °C",
            text_color="#7A7A7A",
            command=self.update_weather_units,
            onvalue=True,
            offvalue=False,
            progress_color="orange",
            fg_color="#444444",
            button_color="white",
            button_hover_color="gray",
            font=ctk.CTkFont(*button_font)
)
        self.unit_switch.pack(side="left", padx=(10, 0)) 
        self.unit_switch.configure(
            text_color=theme_colors[self.current_theme]["button_text"]
        )
        self.use_fahrenheit = not self.unit_switch.get()


        # Theme toggle button that links to the apply theme function(top right corner)
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
        # (city, icon, temp, weather grid)
        self.weather_card = ctk.CTkFrame(
            self.root,
            fg_color="#3A3A3A",
            corner_radius=12,
            border_width=3,
            border_color="#FFA040"  # Orange border around full card
        )
        self.weather_card.pack(pady=(30,10), padx=30, fill='x')

        #  "Last updated" label (moved outside card, below it)
        self.timestamp_label = ctk.CTkLabel(
            master=self.root,
            text="",
            font=ctk.CTkFont(*label_font),
            text_color=theme_colors[self.current_theme]["button_text"]
        )
        self.timestamp_label.pack(pady=(5, 10), anchor="center")

        # ML Prediction label (initially blank)
        self.ml_prediction_label = ctk.CTkLabel(
            master=self.root,
            text="",
            font=ctk.CTkFont("Lucida Bright", 14, "bold"),
            text_color="#FFA040" 
        )
        self.ml_prediction_label.pack(pady=(0, 10), anchor="center")

        # Top row container
        self.card_row = ctk.CTkFrame(self.weather_card, fg_color="transparent")
        self.card_row.pack(padx=20, pady=(20,20))

                # --- Left: City Name + Weather Icon + Temp, Description
        self.left_section = ctk.CTkFrame(
            self.card_row,
            fg_color="#3a3a3a",
            corner_radius=8,
            height=195,
            width=195
        )
        self.left_section.pack(side="left", padx=(0, 8), fill="y",pady=10)
        self.left_section.pack_propagate(False)

        self.city_label = ctk.CTkLabel(
            self.left_section,
            text="Selmer",
            font=ctk.CTkFont(*title_font),
            text_color="#FFA040",
            wraplength=180, 
            justify='center'
        )
        self.city_label.pack(pady=(20, 6),anchor="center", expand=True)

        self.icon_label = tk.Label(
            self.left_section,
            bg="#3a3a3a"
        )
        self.icon_label.pack(pady=(0, 6),anchor="center", expand=True)

        self.temp_desc_label = ctk.CTkLabel(
            self.left_section,
            text="94°F, Very Heavy Rain",
            font=ctk.CTkFont(*label_font),
            text_color="white"
        )
        self.temp_desc_label.pack(pady=(0, 8),anchor="center",expand=True)

        # --- Right: 3x3 weather detail grid
        self.right_section = ctk.CTkFrame(
            self.card_row,
            fg_color="transparent",
            corner_radius=12,
            border_width=1,
            border_color="#444444",
            height=195  # Matches left
        )
        self.right_section.pack(side="left", fill="both", expand=True, padx=(0,10), )
        self.right_section.pack_propagate(False)

# Holds weather stat labels for updates
        self.detail_labels = {}

        grid_keys = [
            "Humidity", "Wind", "Cloudiness",
            "Feels Like", "Pressure", "Visibility",
            "Gusts", "Rain", "Sunrise/Sunset"
        ]

        for idx, key in enumerate(grid_keys):
            row = idx // 3
            col = idx % 3

            stat_frame = ctk.CTkFrame(
                self.right_section,
                fg_color="#3A3A3A",       # same as right_section background
                corner_radius=8,
                border_width=1,
                border_color="#5A5A5A",
                height=50    # subtle border for contrast
            )
            stat_frame.grid(
                row=row,
                column=col,
                padx=2,
                pady=2,
                sticky="nsew"
            )

            label = ctk.CTkLabel(
                stat_frame,
                text=f"{key}: --",  # No icon
                font=ctk.CTkFont("Lucida Bright", 11, "bold"),
                text_color="white",
                fg_color="transparent",
                anchor="w"
            )
            label.pack(fill="both", expand=True, padx=4, pady=2)

            self.detail_labels[key] = label

        # Stretch evenly
        for i in range(3):
            self.right_section.grid_columnconfigure(i, weight=1, uniform="row")

        for i in range(3):
            self.right_section.grid_rowconfigure(i, weight=1, uniform="row")
        # Frame to hold both the map and the buttons side by side
        self.map_and_buttons_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.map_and_buttons_frame.pack(pady=10)

        # Left side: the map
        # self.map_frame = ctk.CTkFrame(self.map_and_buttons_frame, fg_color="#2e2e2e")
        map_bg_color = "#2e2e2e" if self.current_theme == "dark" else "#F2F2F2"

        self.map_frame = ctk.CTkFrame(self.map_and_buttons_frame, fg_color=map_bg_color, border_width=0)
        self.map_frame.pack(side="left", padx=10)

        self.map = MapFeature(self.map_frame)

        # Right side: button column
        self.button_column = ctk.CTkFrame(self.map_and_buttons_frame, fg_color="transparent", border_width=0)
        self.button_column.pack(side="left", padx=10)


# this launches an external live radar map in the browser using folium and rainviewer tiles
        self.radar_button = create_button(
            parent=self.button_column,
            text="Live Radar",
            command=self.open_radar_map,
            theme=self.current_theme
        )
        self.radar_button.pack(pady=10)

# forecast section btn group for 3 5 7 10 16 day forecasts
        self.forecast_button_frame = tk.Frame(self.button_column, bg="#2E2E2E")
        self.forecast_button_frame.pack(pady=5)


# forecast label above button group
        self.forecast_label = ctk.CTkLabel(
            master=self.forecast_button_frame,
            text="Select Daily Forecast",
            font=ctk.CTkFont(*label_font),
            text_color="dark gray"
        )
        self.forecast_label.pack(pady=(5, 2))

        self.forecast_label.configure(
            text_color=theme_colors[self.current_theme]["button_text"]
        )
        # custom seg btn that triggers forecast popup based on selected days
        self.forecast_toggle = create_forecast_segmented_button(
            parent=self.forecast_button_frame,
            on_select_callback=self.handle_forecast_button_click,
            theme="dark"  # or "light"
        )
        self.forecast_toggle.pack(pady=10)


        # Team Viewer button (opens team popup with map + charts)
        self.team_viewer_btn = create_button(
            parent=self.button_column,
            text="Team Viewer",
            command=self.show_team_dashboard,
            theme=self.current_theme
        )
        self.team_viewer_btn.pack(pady=(10, 0))


        # --- Frame to hold the temperature trend chart at the very bottom ---
        # self.temp_chart_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.temp_chart_frame = ctk.CTkFrame(
            self.root,
            fg_color="#3A3A3A",
            corner_radius=12,
            border_width=3,
            border_color="#FFA040",
            height=160 
        )
        self.temp_chart_frame.pack(padx=20, pady=(10, 20), fill="x")


        # Frame to hold the team dashboard (initially hidden)
        self.team_dashboard_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.team_dashboard_frame.pack_forget()


# apply widget styling (defined in setup_styles method)
        # self.setup_styles() 
# bind window close event to clean shutdown handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handles graceful shutdown
# after 100ms auto-fetch weather for the default city ("Selmer") when my app loads
        self.root.after(100, self.get_weather) # fetches weather for selmer(my default)


# get_weather() checks if the user picked a city from autocomplete or typed it in. It fetches weather using the right method, updates the UI with temp, description, icon, and then fills out my 3x3 weather stats grid. It also moves the map to the new location and saves the results to CSV.

    def get_weather(self):
        location = self.city_entry.selected_location

        if location:
            lat = location["lat"]
            lon = location["lon"]
            try:
                weather = fetch_current_weather_by_coords(lat, lon)
                city_name = location.get("label", "Unknown")
            except requests.exceptions.ConnectionError:
                self.show_custom_popup("No Internet", "You're offline or the server can't be reached. Please check your connection.")
                return
            except Exception as e:
                print("[ERROR] Unexpected error during coordinate fetch:", e)
                self.show_custom_popup("Error", "Something went wrong while fetching weather by coordinates.")
                return
        else:
            city = self.city_entry.get().strip()
            if not city:
                city = "Selmer"
            try:
                weather = fetch_current_weather(city)
                city_name = city
            except requests.exceptions.ConnectionError:
                self.show_custom_popup("No Internet", "You're offline or the server can't be reached. Please check your connection.")
                return
            except Exception as e:
                print("[ERROR] Unexpected error during city fetch:", e)
                self.show_custom_popup("Error", "Something went wrong while fetching weather by city.")
                return

        if weather:
            print("[DEBUG] Weather API response says city is:", weather.get("name"))
        else:
            print("[DEBUG] No weather data returned for:", city_name)

        if not weather or "main" not in weather or "weather" not in weather:
            # Handle OpenWeather 404 error properly (city not found)
            if isinstance(weather, dict) and weather.get("cod") == "404":
                message = (
                    f"Oops! '{city_name}' doesn't seem to be a valid city.\n"
                    "Double-check your spelling and try again."
                )
            elif weather is None:
                # Likely offline or connection issue
                message = (
                    f"Could not fetch weather for '{city_name}'.\n"
                    "You may be offline, or there was a problem reaching the API.\n\n"
                    "Try again when you're connected to the internet."
                )
            else:
                message = f"Something went wrong while fetching weather for '{city_name}'."

            self.show_custom_popup("Weather Error", message)
            self.city_entry.focus_set()
            return

        # --- Existing valid weather rendering code ---
        temp_k = weather["main"]["temp"]
        formatted_temp = self.format_temp(temp_k)
        description = weather["weather"][0]["description"].title()
        icon_code = weather["weather"][0]["icon"]
        self.city_label.configure(text=location.get("label", weather["name"]) if location else weather["name"])
        self.temp_desc_label.configure(text=f"{formatted_temp}, {description}")

        icon_image = get_icon_image(icon_code)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image

        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        self.map.update_location(lat, lon)

        for label in self.detail_labels.values():
            label.destroy()
        self.detail_labels.clear()

        # Grid rows...
        self.detail_labels["Humidity"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Humidity')} Humidity: {weather['main']['humidity']}%",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Humidity"].grid(row=0, column=0, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        self.detail_labels["Wind"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Wind')} Wind: {weather['wind']['speed']} mph",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Wind"].grid(row=0, column=1, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        self.detail_labels["Cloudiness"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Cloudiness')} Cloudiness: {weather['clouds']['all']}%",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Cloudiness"].grid(row=0, column=2, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        # Row 1
        feels_like = self.format_temp(weather["main"]["feels_like"])
        self.detail_labels["Feels Like"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Feels Like')} Feels Like: {feels_like}",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Feels Like"].grid(row=1, column=0, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        self.detail_labels["Pressure"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Pressure')} Pressure: {weather['main']['pressure']} hPa",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Pressure"].grid(row=1, column=1, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        self.detail_labels["Visibility"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Visibility')} Visibility: {weather.get('visibility', 0)/1000:.1f} km",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Visibility"].grid(row=1, column=2, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        # Row 2
        wind_gust = weather["wind"].get("gust")
        gust_text = f"{get_detail_icon('Gust')} Gusts: {wind_gust} mph" if wind_gust else "Gusts: N/A"
        self.detail_labels["Wind Gust"] = ctk.CTkLabel(
            self.right_section,
            text=gust_text,
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Wind Gust"].grid(row=2, column=0, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        rain_1h = weather.get("rain", {}).get("1h", 0)
        self.detail_labels["Rain"] = ctk.CTkLabel(
            self.right_section,
            text=f"{get_detail_icon('Rain')} Rain (1h): {rain_1h} mm",
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Rain"].grid(row=2, column=1, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        sunrise_time = datetime.fromtimestamp(weather['sys']['sunrise']).strftime("%I:%M %p")
        sunset_time = datetime.fromtimestamp(weather['sys']['sunset']).strftime("%I:%M %p")
        sunrise_sunset_text = f"{get_detail_icon('Sunrise')} {sunrise_time} / {sunset_time}"
        self.detail_labels["Sunrise/Sunset"] = ctk.CTkLabel(
            self.right_section,
            text=sunrise_sunset_text,
            font=ctk.CTkFont("Lucida Bright", 14),
            text_color="white",
            fg_color="#3A3A3A",
            anchor="w"
        )
        self.detail_labels["Sunrise/Sunset"].grid(row=2, column=2, sticky="w", padx=20, pady=10, ipady=6, ipadx=6)

        save_current_weather_to_csv(weather)

        # Local time and update label
        local_time_str = get_local_time_from_offset(weather.get("timezone", 0))
        last_updated_str = datetime.now().strftime("%I:%M %p")
        self.timestamp_label.configure(
            text=f"{self.city_label.cget('text')} local time: {local_time_str}   |   Last updated: {last_updated_str}"
        )


        # # --- ML Prediction print for Selmer only ---
        print("[DEBUG] City label is:", self.city_label.cget("text"))

        if "Selmer" in self.city_label.cget("text"):
            result = predict_max_temp()
            if result:
                predicted_temp, accuracy = result
                self.ml_prediction_label.configure(
                    text=f"ML Predicted Max Temp for Selmer: {predicted_temp:.1f}°F | Accuracy: {accuracy}%"
                )
            else:
                self.ml_prediction_label.configure(text="")
        else:
            self.ml_prediction_label.configure(text="")

        

        # --- Forecast Chart ---
        forecast = fetch_forecast(self.city_label.cget("text"))
        
      
        if forecast and "list" in forecast:
            try:
               
                temps_raw = self.extract_hourly_temps(forecast, hours=8)
                temps = [self.format_temp_value_only(temp_k) for temp_k in temps_raw]
                for widget in self.temp_chart_frame.winfo_children():
                    widget.destroy()
                inner_chart_frame = ctk.CTkFrame(self.temp_chart_frame, fg_color="transparent")
                inner_chart_frame.pack(padx=10, pady=14, fill="both", expand=True)
                offset_seconds = weather.get("timezone", 0)
                now_utc = datetime.utcnow()
                time_labels = [
                    (now_utc + timedelta(hours=i) + timedelta(seconds=offset_seconds)).strftime("%I %p")
                    for i in range(8)
                ]
                unit = "°F" if self.use_fahrenheit else "°C"
                display_temperature_chart(inner_chart_frame, temps, time_labels,unit)
            except Exception as e:
                print(f"[ERROR] Failed to process temperature chart: {e}")
        else:
            print(f"[DEBUG] Forecast not available or invalid for {self.city_label.cget('text')}")



    def extract_hourly_temps(self, forecast_data, hours=8):
        temps = []
        if "list" in forecast_data:
            for entry in forecast_data["list"][:hours]:
                temp_k = entry["main"]["temp"]
                temps.append(round(temp_k))
        return temps


    def open_radar_map(self):
        location = self.city_entry.selected_location

        if location:
            lat = location["lat"]
            lon = location["lon"]
            launch_radar_map_by_coords(lat, lon)
        else:
            city = self.city_entry.get().strip().split(",")[0]
            if not city:
                self.show_custom_popup("Missing City", "Please enter a city before launching radar.")
                return
            launch_radar_map_by_name(city)



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
        # style.configure("TFrame", background=bg_color)
        map_bg_color = "#2e2e2e" if theme_name == "dark" else "#F9f6f3"
        self.map_frame.configure(fg_color=map_bg_color, border_width=0)
        self.button_column.configure(fg_color=map_bg_color, border_width=0)
        self.forecast_button_frame.configure(bg=map_bg_color)

        self.map_and_buttons_frame.configure(fg_color=bg_color)

        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TEntry", fieldbackground=card_bg, background=card_bg, foreground=fg_color)
        style.configure("TButton", background=card_bg, foreground=fg_color)

        style.configure("InputRow.TFrame", background=bg_color)
        self.timestamp_label.configure(
            text_color=theme_colors[self.current_theme]["button_text"]
        )
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

        
        self.unit_switch.configure(
            text_color=theme_colors[self.current_theme]["button_text"]
        )

        self.forecast_label.configure(
            text_color=theme_colors[self.current_theme]["button_text"]
        )
        # Regular Tk widgets (logo + toggle container)
        self.theme_toggle_container.configure(bg=bg_color)
        self.logo_label.configure(bg=bg_color)

        # Map frame (ttk)


        # Always use dark style for weather card (even in light mode)
        self.weather_card.configure(fg_color="#3A3A3A", border_color="#FFA040", border_width=2)
 
        if hasattr(self, "left_card"):
            self.left_card.configure(fg_color="#2E2E2E")
        if hasattr(self, "right_card"):
            self.right_card.configure(fg_color="#3A3A3A")


        self.theme_toggle.update_style(theme_name)


    # def handle_forecast_button_click(self, days):
        # get city from the input field
    def handle_forecast_button_click(self, days):
        threading.Thread(target=self._run_forecast_logic, args=(days,), daemon=True).start()



    def _run_forecast_logic(self, days):
        print(f"[DEBUG] Running forecast logic for {days}-day forecast")

        location = self.city_entry.selected_location
        coords = None
        city_label = None
        if location:
            coords = (location["lat"], location["lon"])
            city_label = location.get("label", "Unknown")
        else:
            city_label = self.city_entry.get().strip() or "Selmer"
            print(f"[DEBUG] No selected_location found. Defaulting to city name only: {city_label}")

            # Try to geocode it manually using geopy
            try:
                geolocator = Nominatim(user_agent="volunteer_weather_app")
                geo_location = geolocator.geocode(city_label)
                if geo_location:
                    coords = (geo_location.latitude, geo_location.longitude)
                    print(f"[DEBUG] Manual geocoding success: {coords}")
                else:
                    print("[DEBUG] Geocoding failed")
            except Exception as e:
                print("[DEBUG] Geocoding error:", e)

        print(f"[DEBUG] City entry: {city_label}")
        print(f"[DEBUG] Coordinates: {coords}")

        if days in [3, 5]:
            print("[DEBUG] Fetching short-range forecast")
            forecast = fetch_forecast(city_label)
            if not forecast or "list" not in forecast:
                self.show_custom_popup("Forecast Error", f"Could not retrieve forecast for '{city_label}'.")
                return
            forecast_summary = process_forecast_data(forecast, days)
        else:
            print("[DEBUG] Fetching extended forecast")
            if coords:
                lat, lon = coords
                forecast = fetch_extended_forecast(lat, lon, days)
            else:
                print("[DEBUG] No coordinates available for extended forecast.")
                self.show_custom_popup("Location Error", f"Coordinates are required for a {days}-day forecast.")
                return

            if not forecast or "list" not in forecast:
                print("[DEBUG] Extended forecast failed")
                self.show_custom_popup("Extended Forecast Error", f"Could not retrieve extended forecast for '{city_label}'.")
                return

            forecast_summary = process_extended_forecast_data(forecast, days)

        # Pad forecast to match expected days (for chart layout)
        while len(forecast_summary) < days:
            forecast_summary.append({
                "date": f"Day +{len(forecast_summary) + 1}",
                "high": "--", "low": "--",
                "desc": "Predicted Day", "icon": "01d"
            })

        print(f"[DEBUG] Final forecast summary ({len(forecast_summary)} days):", forecast_summary)

        self.root.after(0, lambda: show_forecast_popup(
            self.root,
            city_label,
            forecast_summary,
            days,
            theme=self.current_theme,
            format_temp_func=self.format_temp
        ))


    def show_custom_popup(self, title, message):
        # create a new popup window like a mini alert box
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#3A3A3A")
        # Center the popup on the main window
        popup_width = 300
        popup_height = 150

        self.root.update_idletasks()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        x = root_x + (root_width // 2) - (popup_width // 2)
        y = root_y + (root_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False) #lock window size
# add the message label in the center of the popup
        label = tk.Label(
            popup,
            text=message,
            font=popup_font,
            fg="white",
            bg="#3A3A3A",
            wraplength=280,
            justify="center"
        )
        label.pack(pady=20, padx=10)
# ok btn that closes the popup
        close_button = tk.Button(
            popup,
            text="OK",
            command=popup.destroy,
            bg="#5a5a5a",
            fg="white",
            font=popup_font,
            relief="flat",
            activebackground="#777777",
            activeforeground="white"
        )
        close_button.pack(pady=10)
# set popup behavior stay on top and wait for it to close before continuing
        popup.transient(self.root) #ties popup to main window
        popup.grab_set() #block interactio with main window
        self.root.wait_window(popup) #pause program until popup is closed



    def format_temp(self, temp):
        # try to safely convert the input to a float
        try:
            temp = float(temp)  # Fixes the bug!
        except ValueError:
            return "N/A" #return fallback if conversion fails
# convert temp based on selected unit (f or c)
        if self.use_fahrenheit:
            return f"{round(temp)}°F"
        else:
            celsius = (temp - 32) * 5 / 9
            return f"{round(celsius)}°C"
        
    def format_temp_value_only(self, temp):
        try:
            temp = float(temp)
        except ValueError:
            return None
        if self.use_fahrenheit:
            return round(temp)
        else:
            celsius = (temp - 32) * 5 / 9
            return round(celsius)


    def update_weather_units(self):
        # toggles between fahrenheit and celsius
        self.use_fahrenheit = not self.unit_switch.get()  # True = °F, False = °C
        self.get_weather()  # makes the temp update right away

        # ✅ If team dashboard is showing, update it too
        if self.team_dashboard_frame.winfo_ismapped():
            render_team_dashboard(
                parent_frame=self.team_dashboard_frame,
                csv_path="team_7_Folder/team_weather_data.csv",
                theme=ctk.get_appearance_mode().lower(),
                unit="Fahrenheit" if self.use_fahrenheit else "Celsius",
                show_main_callback=self.render_main_view
            )

    def show_team_dashboard(self):
        # Hide all other main window sections
        self.weather_card.pack_forget()
        self.timestamp_label.pack_forget()
        self.map_and_buttons_frame.pack_forget()
        self.temp_chart_frame.pack_forget()

        # Show the team dashboard frame
        self.team_dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        #  Always get current theme dynamically
        render_team_dashboard(
            parent_frame=self.team_dashboard_frame,
            csv_path="team_7_Folder/team_weather_data.csv",
            theme=ctk.get_appearance_mode().lower(),
            show_main_callback=self.render_main_view
        )

    def render_main_view(self):
        self.team_dashboard_frame.pack_forget()
        self.weather_card.pack(pady=10)
        self.timestamp_label.pack()
        self.map_and_buttons_frame.pack(pady=10, anchor='center')
        self.map_frame.pack_forget()
        self.button_column.pack_forget()
        self.map_frame.pack(side="left", padx=10)
        self.button_column.pack(side="left", padx=10)
        self.temp_chart_frame.pack(fill="x", padx=10, pady=(0, 10))

    def show_team_dashboard(self):
        # Hide all other main window sections
        self.weather_card.pack_forget()
        self.timestamp_label.pack_forget()
        self.map_and_buttons_frame.pack_forget()
        self.temp_chart_frame.pack_forget()

        # Show the team dashboard frame
        self.team_dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Always get current theme and unit dynamically
        render_team_dashboard(
            parent_frame=self.team_dashboard_frame,
            csv_path="team_7_Folder/team_weather_data.csv",
            theme=ctk.get_appearance_mode().lower(),
            unit="Fahrenheit" if self.use_fahrenheit else "Celsius",  # ✅ pass unit!
            show_main_callback=self.render_main_view
        )



    def on_close(self):
        # try to safely destroy the map to avoid errors on exit
        try:
            self.map.destroy()
        except Exception as e:
            print("Map cleanup error:", e)
# delay app exit slightly to avoid crashing threads, then force exit
        self.root.after(100, self.root.destroy)  #Slight delay to avoid crashing background threads
        os._exit(0) #completely shuts down the app(including background threads)
















        

















