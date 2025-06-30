import tkinter as tk
from tkinter import ttk
from datetime import datetime
from core.api import fetch_current_weather, fetch_forecast
from core.icons import get_icon_image, get_detail_icon
from features.storage import save_current_weather_to_csv, save_forecast_to_csv

from features.dark_light_mode import ThemeToggle 

from features.map_feature import MapFeature


import subprocess
import sys
import os
from tkinter import messagebox

# for logo
from PIL import Image, ImageTk, ImageDraw


from gui.forecast_popups import show_forecast_popup, process_forecast_data

from features.radar_launcher import launch_radar_map


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("AChurchwell-TPS2025-Capstone")
        self.root.geometry("1000x950")
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.current_theme = "dark"

        self.city_var = tk.StringVar(value='Selmer')

        # --- Centered Search Row ---
        self.input_container = ttk.Frame(root, style="InputRow.TFrame")
        self.input_container.pack(pady=10)

        self.input_frame = ttk.Frame(self.input_container)
        self.input_frame.pack(anchor='center')


        # --- Logo Section (circular + centered under search bar) ---


        logo_path = os.path.join("assets", "icons", "snakebit_skies.png")
        logo_raw = Image.open(logo_path).resize((120, 120))
        self.logo_img = ImageTk.PhotoImage(logo_raw)


        # Display logo centered under the input frame
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg="#2E2E2E")
        self.logo_label.pack(pady=(10, 0))


        # City input
        self.city_entry = tk.Entry(
            self.input_frame,
            textvariable=self.city_var,
            font=("Segoe UI", 10),
            fg="white",
            bg="#444444",
            insertbackground="white",
            width=30,
            relief="flat",
            highlightthickness=0,
            bd=0
        )
        self.city_entry.pack(side="left", padx=(0, 5), ipady=5)

        # Search button
        self.search_button = tk.Button(
            self.input_frame,
            text="Search",
            command=self.get_weather,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#ff6f00",
            activebackground="#ffa040",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=5
        )
        self.search_button.pack(side="right")

        # Theme toggle button (floating in top-right corner)
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
        self.weather_card = ttk.Frame(root, padding=10, style="MainCard.TFrame")
        self.weather_card.pack(pady=10, fill="x", padx=10)

        self.city_label = ttk.Label(self.weather_card, text="", style="CityTitle.TLabel")
        self.city_label.grid(row=0, column=0, sticky="w", padx=5)

        self.icon_label = tk.Label(self.weather_card, bg="#3a3a3a")
        self.icon_label.grid(row=0, column=1, rowspan=2, padx=10)

        self.temp_desc_label = ttk.Label(self.weather_card, text="", style="Condition.TLabel")
        self.temp_desc_label.grid(row=1, column=0, sticky="w", padx=5)

        self.detail_labels = {}
        for i, key in enumerate(["Humidity", "Wind", "Cloudiness", "Visibility"]):
            row = 2 + i // 2
            col = i % 2
            label = ttk.Label(self.weather_card, text=f"{get_detail_icon(key)} {key}: --", style="Detail.TLabel")
            label.grid(row=row, column=col, sticky="w", padx=10, pady=5)
            self.detail_labels[key] = label


        # Add map frame and map widget
        self.map_frame = ttk.Frame(self.root)
        self.map_frame.pack(pady=10)

        self.map = MapFeature(self.map_frame)


# leave this out for now bc i dont wanna show this!!!!! But ITS DEF GOING IN MY CAPSTONE SO DONOT DELETE ANDREA!!!!
        self.radar_button = tk.Button(
            self.root,
            text="Live Radar",
            command=self.open_radar_map,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#FF6F00",
            activebackground="#FFA040",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=5
        )
        self.radar_button.pack(pady=10)


                # Forecast buttons
        forecast_button_frame = tk.Frame(self.root, bg="#2E2E2E")
        forecast_button_frame.pack(pady=5)

        tk.Button(
            forecast_button_frame, text="3-Day Forecast", command=lambda: self.show_forecast_popup(3),
            font=("Segoe UI", 10, "bold"), fg="white", bg="#5a5a5a",
            activebackground="#777777", activeforeground="white",
            relief="flat", bd=0, padx=10, pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            forecast_button_frame, text="5-Day Forecast", command=lambda: self.show_forecast_popup(5),
            font=("Segoe UI", 10, "bold"), fg="white", bg="#5a5a5a",
            activebackground="#777777", activeforeground="white",
            relief="flat", bd=0, padx=10, pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            forecast_button_frame, text="7-Day Forecast", command=lambda: self.show_forecast_popup(7),
            font=("Segoe UI", 10, "bold"), fg="white", bg="#5a5a5a",
            activebackground="#777777", activeforeground="white",
            relief="flat", bd=0, padx=10, pady=5
        ).pack(side="left", padx=5)



        self.setup_styles()
        self.root.after(100, self.get_weather)

    def setup_styles(self):
        style = ttk.Style()

        style.configure("MainCard.TFrame", background="#3a3a3a", relief="solid", borderwidth=2)
        style.configure("CityTitle.TLabel", background="#3a3a3a", foreground="#ffa040", font=("Segoe UI", 18, "bold"))
        style.configure("Condition.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 11))
        style.configure("Detail.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10))



    def get_weather(self):
        city = self.city_var.get().strip()

        if not city:
            messagebox.showwarning(
                "Missing City",
                "Please enter a city name to get weather data."
            )
            self.city_entry.focus_set()
            return

        weather = fetch_current_weather(city)
       

        if not weather or "main" not in weather or "weather" not in weather:
            messagebox.showerror(
                "City Not Found",
                f"Oops! '{city}' doesn't seem to be a real city.\nDouble-check your spelling and try again."
            )
            self.city_entry.focus_set()
            return

        # --- Proceed if city is valid ---
        temp = weather["main"]["temp"]
        description = weather["weather"][0]["description"].title()
        icon_code = weather["weather"][0]["icon"]

        self.city_label.config(text=weather["name"])
        self.temp_desc_label.config(text=f"{temp}°F, {description}")

        icon_image = get_icon_image(icon_code)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image

        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        self.map.update_location(lat, lon)

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

        save_current_weather_to_csv(weather)

    def open_radar_map(self):
        city = self.city_var.get().strip()
        launch_radar_map(city, self.show_custom_popup)







    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        print(f"Theme switched to: {theme_name}")

        if theme_name == "dark":
            bg_color = "#2E2E2E"
            fg_color = 	"#EBE8E5FF"
            card_bg = "#3A3A3A"
        else:  # light
            bg_color = "#C6C2C2"
            fg_color = "#2E2E2E"
            card_bg = "#C6C2C2"

        # Update root background
        self.root.configure(bg=bg_color)

        # Update styles (you may have set these earlier using ttk.Style)
        style = ttk.Style()

        # General frame style
        style.configure("TFrame", background=bg_color)

        # Labels
        style.configure("TLabel", background=bg_color, foreground=fg_color)

        # Entry and Buttons
        style.configure("TEntry", fieldbackground=card_bg, background=card_bg, foreground=fg_color)
        style.configure("TButton", background=card_bg, foreground=fg_color)

        # If you created custom styles (like "InputRow.TFrame", etc.), update those too
        style.configure("InputRow.TFrame", background=bg_color)  



    def show_custom_popup(self, title, message):
            popup = tk.Toplevel(self.root)
            popup.title(title)
            popup.configure(bg="#3A3A3A")
            popup.geometry("300x150")
            popup.resizable(False, False)

            label = tk.Label(popup, text=message, font=("Segoe UI", 10), fg="white", bg="#3A3A3A", wraplength=280, justify="center")
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


    def show_forecast_popup(self, days):
        city = self.city_var.get().strip()
        if not city:
            self.show_custom_popup("Missing City", "Please enter a city before viewing the forecast.")
            return

        forecast = fetch_forecast(city)
        if not forecast or "list" not in forecast:
            self.show_custom_popup("Forecast Error", f"Could not retrieve forecast data for '{city}'.")
            return

        forecast_summary = process_forecast_data(forecast, days)

        while len(forecast_summary) < days:
            forecast_summary.append({
                "date": f"Day +{len(forecast_summary) + 1}",
                "high": "--", "low": "--",
                "desc": "Predicted Day", "icon": "01d"
            })

        show_forecast_popup(self.root, city, forecast_summary, days)
















