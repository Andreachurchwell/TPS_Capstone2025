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

from features.custom_buttons import create_button
import customtkinter as ctk


class MainWindow:
    def __init__(self, root):

        # makes the main app window
        self.root = root
        self.root.title("AChurchwell-TPS2025-Capstone")
        self.root.geometry("1000x950") # sets my window size
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.current_theme = "dark"    # makes it start it dark mode

        # self.city_var = tk.StringVar(value='Selmer') # makes selmer my original city
        self.city_var = tk.StringVar() # makes selmer my original city

        # --- Centered Search Row ---
        self.input_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_container.pack(pady=10)

        self.input_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.input_frame.pack(anchor='center')
        self.city_entry = ctk.CTkEntry(
            master=self.input_frame,
            placeholder_text="Enter city...",
            width=240,
            height=32,
            font=ctk.CTkFont("Segoe UI", 12),
            textvariable=self.city_var
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
        logo_raw = Image.open(logo_path).resize((120, 120))
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
        # main card displays my weather details
        self.weather_card = ttk.Frame(root, padding=10, style="MainCard.TFrame")
        self.weather_card.pack(pady=10, fill="x", padx=10)


        # my label to show the name of the selected city
        self.city_label = ttk.Label(self.weather_card, text="", style="CityTitle.TLabel")
        self.city_label.grid(row=0, column=0, sticky="w", padx=5)
        # image placeholder for weather icon
        self.icon_label = tk.Label(self.weather_card, bg="#3a3a3a")
        self.icon_label.grid(row=0, column=1, rowspan=2, padx=10)
        # my label to show temp and weather descriptions
        self.temp_desc_label = ttk.Label(self.weather_card, text="", style="Condition.TLabel")
        self.temp_desc_label.grid(row=1, column=0, sticky="w", padx=5)


        # creates a dictionary to hold additional deatails
        self.detail_labels = {}
        # loops thru dets and creates labels for em
        for i, key in enumerate(["Humidity", "Wind", "Cloudiness", "Visibility"]):
            row = 2 + i // 2
            col = i % 2
            label = ttk.Label(self.weather_card, text=f"{get_detail_icon(key)} {key}: --", style="Detail.TLabel")
            label.grid(row=row, column=col, sticky="w", padx=10, pady=5)
            self.detail_labels[key] = label  #store refs for later updates


        # Add map frame and map widget
        self.map_frame = ttk.Frame(self.root)
        self.map_frame.pack(pady=10)
        # makes map widget using custom mapfeature class
        self.map = MapFeature(self.map_frame)

        


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


        for days in [3, 5, 7,10, 16]:
            btn = create_button(
                parent=self.forecast_button_frame,
                text=f"{days}-Day Forecast",
                command=lambda d=days: self.handle_forecast_button_click(d),
                theme=self.current_theme
            )
            btn.pack(side="left", padx=5)



        self.setup_styles() # applies custom widget style

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handles graceful shutdown

        self.root.after(100, self.get_weather) # fetches weather for selmer(my default)





    def setup_styles(self):
        style = ttk.Style()
# style for main weather card
        style.configure("MainCard.TFrame", background="#3a3a3a", relief="solid", borderwidth=2)
# style for city name label thats big and bold
        style.configure("CityTitle.TLabel", background="#3a3a3a", foreground="#ffa040", font=("Segoe UI", 18, "bold"))
# style for temp and condition label
        style.configure("Condition.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 11))
# style for all the detail labels
        style.configure("Detail.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10))



    def get_weather(self):
        # get current city name from the entry field
        city = self.city_var.get().strip()
        
        # if nothing typed, fall back to Selmer
        if not city:
            city = "Selmer"  # fallback default

        # calling the api to fetch weather for the city
        weather = fetch_current_weather(city)
        
        # if api fails or invalid city, show popup error
        if not weather or "main" not in weather or "weather" not in weather:
            messagebox.showerror(
                "City Not Found",
                f"Oops! '{city}' doesn't seem to be a real city.\nDouble-check your spelling and try again."
            )
            self.city_entry.focus_set()
            return

        # if data is valid, get temp, description, and icon code
        temp_k = weather["main"]["temp"]
        formatted_temp = self.format_temp(temp_k)
        description = weather["weather"][0]["description"].title()
        icon_code = weather["weather"][0]["icon"]

        # update the city name and temp/desc and icon
        self.city_label.config(text=weather["name"])
        self.temp_desc_label.config(text=f"{formatted_temp}, {description}")

        # get weather icon and display it
        icon_image = get_icon_image(icon_code)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image  # prevents image garbage collection

        # update map location
        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        self.map.update_location(lat, lon)

        # updates weather details
        self.detail_labels["Humidity"].config(
            text=f"{get_detail_icon('Humidity')} Humidity: {weather['main']['humidity']}%"
        )
        self.detail_labels["Wind"].config(
            text=f"{get_detail_icon('Wind')} Wind: {weather['wind']['speed']} mph"
        )
        self.detail_labels["Cloudiness"].config(
            text=f"{get_detail_icon('Cloudiness')} Cloudiness: {weather['clouds']['all']}%"
        )
        self.detail_labels["Visibility"].config(
            text=f"{get_detail_icon('Visibility')} Visibility: {weather.get('visibility', 0)/1000:.1f} km"
        )

                # Optionally add more details below:
        feels_like = self.format_temp(weather["main"]["feels_like"])
        self.detail_labels["Feels Like"] = ttk.Label(
            self.weather_card,
            text=f"🌡️ Feels Like: {feels_like}",
            style="Detail.TLabel"
        )
        self.detail_labels["Feels Like"].grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.detail_labels["Pressure"] = ttk.Label(
            self.weather_card,
            text=f"📈 Pressure: {weather['main']['pressure']} hPa",
            style="Detail.TLabel"
        )
        self.detail_labels["Pressure"].grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Optional wind gust
        wind_gust = weather["wind"].get("gust")
        if wind_gust:
            self.detail_labels["Wind Gust"] = ttk.Label(
                self.weather_card,
                text=f"💨 Gusts: {wind_gust} mph",
                style="Detail.TLabel"
            )
            self.detail_labels["Wind Gust"].grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Optional rain
        rain_1h = weather.get("rain", {}).get("1h")
        if rain_1h:
            self.detail_labels["Rain"] = ttk.Label(
                self.weather_card,
                text=f"🌧️ Rain (1h): {rain_1h} mm",
                style="Detail.TLabel"
            )
            self.detail_labels["Rain"].grid(row=5, column=1, sticky="w", padx=10, pady=5)

        sunrise_time = datetime.fromtimestamp(weather['sys']['sunrise']).strftime("%I:%M %p")
        sunset_time = datetime.fromtimestamp(weather['sys']['sunset']).strftime("%I:%M %p")
        print("Sunrise:", sunrise_time)
        print("Sunset:", sunset_time)
        # saves to csv file
        save_current_weather_to_csv(weather)



    def open_radar_map(self):
        # get city from the entry
        city = self.city_var.get().strip()
        # launch radar map in browser using a helper function
        # passes in self.showcustom in case the city is invalid
        launch_radar_map(city, self.show_custom_popup)






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
        self.city_entry.configure(
            fg_color=card_bg,
            text_color=fg_color,
            placeholder_text_color="#AAAAAA" if theme_name == "light" else "#CCCCCC"
        )
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








    # def handle_forecast_button_click(self, days):
    #     city = self.city_var.get().strip()
    #     if not city:
    #         city = 'Selmer'

    #     forecast = fetch_forecast(city)
    #     if not forecast or "list" not in forecast:
    #         self.show_custom_popup("Forecast Error", f"Could not retrieve forecast data for '{city}'.")
    #         return

    #     save_forecast_to_csv(forecast)
    #     forecast_summary = process_forecast_data(forecast, days)

    #     # Save to database
    #     formatted_forecast = []
    #     for day in forecast_summary:
    #         if day["high"] == "--":
    #             continue
    #         formatted_forecast.append({
    #             "date": day["date"],
    #             "min_temp": day["low"],
    #             "max_temp": day["high"],
    #             "humidity": 55,
    #             "wind_speed": 5.2,
    #             "description": day["desc"],
    #             "icon_code": day["icon"]
    #         })
    #     save_forecast_to_db(city, formatted_forecast)

    #     while len(forecast_summary) < days:
    #         forecast_summary.append({
    #             "date": f"Day +{len(forecast_summary) + 1}",
    #             "high": "--", "low": "--",
    #             "desc": "Predicted Day", "icon": "01d"
    #         })


    #     # show_forecast_popup(self.root, city, forecast_summary, days, self.current_theme, self.format_temp)
    #     show_forecast_popup(
    #         self.root,
    #         city,
    #         forecast_summary,
    #         days,
    #         theme=self.current_theme,
    #         format_temp_func=self.format_temp
    #     )


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

















