import tkinter as tk
from tkinter import ttk
from datetime import datetime
from core.api import fetch_current_weather, fetch_forecast, fetch_extended_forecast
from core.icons import get_icon_image, get_detail_icon
from features.storage import save_current_weather_to_csv, save_forecast_to_csv
from features.dark_light_mode import ThemeToggle 
from features.map_feature import MapFeature

from tkinter import messagebox
# for logo
from PIL import Image, ImageTk

import customtkinter as ctk

import os

from gui.forecast_popups import show_forecast_popup, process_forecast_data,process_extended_forecast_data
# from features.radar_launcher import launch_radar_map
from core.weather_database import save_forecast_to_db
from features.custom_buttons import create_button, create_forecast_segmented_button
from features.autocomplete import AutocompleteEntry
from core.api import fetch_current_weather_by_coords

from features.radar_launcher import launch_radar_map_by_coords, launch_radar_map_by_name
from features.temp_trend_chart import display_temperature_chart

# from core.api import fetch_air_quality
import threading
import time
from geopy.geocoders import Nominatim




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
            font=("Segoe UI", 12),
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
        self.weather_card.pack(pady=(30,20), padx=30)

        # Top row container
        self.card_row = ctk.CTkFrame(self.weather_card, fg_color="transparent")
        self.card_row.pack(padx=20, pady=(20,20))

                # --- Left: City Name + Weather Icon + Temp, Description
        self.left_section = ctk.CTkFrame(
            self.card_row,
            fg_color="#3a3a3a",
            corner_radius=8,

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

        # --- Right: 3x3 weather detail grid
        self.right_section = ctk.CTkFrame(
            self.card_row,
            fg_color="#3a3a3a",
            corner_radius=12,
            border_width=1,
            border_color="#444444"  # Matches left
        )
        self.right_section.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

    #    will hold weather stat labels for updates
        self.detail_labels = {}

        grid_keys = [
            "Humidity", "Wind", "Cloudiness",
            "Feels Like", "Pressure", "Visibility",
            "Gusts", "Rain", "Sunrise/Sunset"
        ]
# gives me both indexnum and value from the list exp. 0,1,2 'humidity' 'wind'
# enumerate() lets me loop through each weather stat with a counter, so I can calculate what row and column to put it in.
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

# # # timestamp
        self.timestamp_label = ctk.CTkLabel(
            master=self.card_row,
            text="",
            font=("Segoe UI", 12),
            text_color="lightgray"
        )
        self.timestamp_label.pack(pady=(10, 5), anchor='e')



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
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color="dark gray"
        )
        self.forecast_label.pack(pady=(5, 2))
        # custom seg btn that triggers forecast popup based on selected days
        self.forecast_toggle = create_forecast_segmented_button(
            parent=self.forecast_button_frame,
            on_select_callback=self.handle_forecast_button_click,
            theme="dark"  # or "light"
        )
        self.forecast_toggle.pack(pady=10)



        # --- Frame to hold the temperature trend chart at the very bottom ---
        # self.temp_chart_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.temp_chart_frame = ctk.CTkFrame(
            self.root,
            fg_color="#3A3A3A",
            corner_radius=12,
            border_width=3,
            border_color="#FFA040"
        )
        self.temp_chart_frame.pack(padx=20, pady=(10, 20), fill="x")


# apply widget styling (defined in setup_styles method)
        self.setup_styles() 
# bind window close event to clean shutdown handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handles graceful shutdown
# after 100ms auto-fetch weather for the default city ("Selmer") when my app loads
        self.root.after(100, self.get_weather) # fetches weather for selmer(my default)





    def setup_styles(self):
        style = ttk.Style()
# style for main weather card background
        # style.configure("MainCard.TFrame", background="#3a3a3a", relief="flat", borderwidth=1)
# style for city name label thats big and bold
        style.configure("CityTitle.TLabel", background="#3a3a3a", foreground="#ffa040", font=("Segoe UI", 22, "bold"))
# style for temp and weather condition label
        style.configure("Condition.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 14,'bold'))
# style for all the detail labels
        style.configure("Detail.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10))

# get_weather() checks if the user picked a city from autocomplete or typed it in. It fetches weather using the right method, updates the UI with temp, description, icon, and then fills out my 3x3 weather stats grid. It also moves the map to the new location and saves the results to CSV.

    def get_weather(self):
    #   first check if a city was selected from autocomplete(has coordinates)
        location = self.city_entry.selected_location

        if location:
        #    fetch weather by coodinates(more accurate)
            lat = location["lat"]
            lon = location["lon"]
            weather = fetch_current_weather_by_coords(lat, lon)
            city_name = location.get("label", "Unknown")  # For debug or error messages
            
        else:
            # no location selected, fallback to typed city name
            #  User typed a city name manually
            city = self.city_entry.get().strip()
            if not city:
                city = "Selmer"  #default city if nothing is entered
            weather = fetch_current_weather(city)
            city_name = city  # For debug or error messages

        #  Debug print to see what city the api returned
        if weather:
            print("[DEBUG] Weather API response says city is:", weather.get("name"))
        else:
            print("[DEBUG] No weather data returned for:", city_name)

    #  if api failed or response is missing expected fields, show an error
        if not weather or "main" not in weather or "weather" not in weather:
            messagebox.showerror(
                "City Not Found",
                f"Oops! '{city_name}' doesn't seem to be a real city.\nDouble-check your spelling and try again."
            )
            self.city_entry.focus_set()
            return

# if weather data is valid, update the UI
        temp_k = weather["main"]["temp"]
        formatted_temp = self.format_temp(temp_k)
        description = weather["weather"][0]["description"].title()
        icon_code = weather["weather"][0]["icon"]
# update city name label
        self.city_label.configure(text=location.get("label", weather["name"]) if location else weather["name"])
# update temp and condition label
        self.temp_desc_label.configure(text=f"{formatted_temp}, {description}")

# update weather icon image
        icon_image = get_icon_image(icon_code)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image  # Keep a reference to avoid garbage collection

# update map position
        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        self.map.update_location(lat, lon)

# clear out old grid labels before adding new ones
        for label in self.detail_labels.values():
            label.destroy()
        self.detail_labels.clear()

# add updated weather into into 3X3 grid
# row 0
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

# save the weather to csv file (for future use or tracking)

# comment out for now to see if its why my app is slow 7-19!!!!!!
        # save_current_weather_to_csv(weather)


        # Add a "Last updated" timestamp to the UI

        now = datetime.now().strftime("%I:%M %p")  # or full format if you want
        self.timestamp_label.configure(text=f"Last updated: {now}")


        # --- Get forecast and display temperature trend chart ---
        forecast = fetch_forecast(self.city_label.cget("text"))
        if forecast:
            temps = self.extract_hourly_temps(forecast, hours=8)
            # Clear existing chart if needed (optional: not required if just redrawing)
            # for widget in self.temp_chart_frame.winfo_children():
            #     widget.destroy()
            # # Draw the new chart
            # display_temperature_chart(self.temp_chart_frame, temps)

            # Clear old chart
        for widget in self.temp_chart_frame.winfo_children():
            widget.destroy()

        # Create inner frame so border isn't hidden
        inner_chart_frame = ctk.CTkFrame(
            self.temp_chart_frame,
            fg_color="transparent"
        )
        inner_chart_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Display chart inside the inner frame
        display_temperature_chart(inner_chart_frame, temps)

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

#         city = self.city_var.get().strip()
#         if not city:
#             city = 'Selmer'#default is nothing is entered
# # short range (3/5 days)
#         if days in [3, 5]:  # ← these use standard 3-hour forecast
#             forecast = fetch_forecast(city)
#             # if the api failed or didnt return data, show this error
#             if not forecast or "list" not in forecast:
#                 self.show_custom_popup("Forecast Error", f"Could not retrieve forecast data for '{city}'.")
#                 return
# # save raw forcast to csv file
#             save_forecast_to_csv(forecast)
# # summarize the raw forecast in to daily high/low plus icon and description
#             forecast_summary = process_forecast_data(forecast, days)
# # extended range(7,10,16)
#         else:  # ← 7, 10, 16 use extended forecast
#             forecast = fetch_extended_forecast(city, days)
#         # if api call failed show error
#             if not forecast or "list" not in forecast:
#                 self.show_custom_popup("Extended Forecast Error", f"Could not retrieve extended forecast for '{city}'.")
#                 return
# # summarize extended forecast into daily high/low 
#             forecast_summary = process_extended_forecast_data(forecast, days)

#         # format data for saving to sqlite database
#         formatted_forecast = []
#         for day in forecast_summary:
#             if day["high"] == "--":
#                 continue #skip empty placeholders
#             formatted_forecast.append({
#                 "date": day["date"],
#                 "min_temp": day["low"],
#                 "max_temp": day["high"],
#                 "humidity": 55,
#                 "wind_speed": 5.2,
#                 "description": day["desc"],
#                 "icon_code": day["icon"]
#             })
#             # save to local database for long term storage
#         save_forecast_to_db(city, formatted_forecast)
# # fill in any missing days with placeholders so charts display evenly
#         while len(forecast_summary) < days:
#             forecast_summary.append({
#                 "date": f"Day +{len(forecast_summary) + 1}",
#                 "high": "--", "low": "--",
#                 "desc": "Predicted Day", "icon": "01d"
#             })
# # display popup with forecast summary and visual chart
#         show_forecast_popup(
#             self.root,
#             city,
#             forecast_summary,
#             days,
#             theme=self.current_theme,
#             format_temp_func=self.format_temp
#         )

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

            # ✅ Try to geocode it manually using geopy
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
        popup.geometry("300x150")
        popup.resizable(False, False) #lock window size
# add the message label in the center of the popup
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
# ok btn that closes the popup
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


    def update_weather_units(self):
        # toggles between fahrenheit and celsius
        self.use_fahrenheit = not self.unit_switch.get()  # True = °F, False = °C
        self.get_weather()  # makes the temp update right away


    def on_close(self):
        # try to safely destroy the map to avoid errors on exit
        try:
            self.map.destroy()
        except Exception as e:
            print("Map cleanup error:", e)
# delay app exit slightly to avoid crashing threads, then force exit
        self.root.after(100, self.root.destroy)  #Slight delay to avoid crashing background threads
        os._exit(0) #completely shuts down the app(including background threads)












        

















