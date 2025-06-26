import tkinter as tk
from tkinter import ttk
from core.api import fetch_current_weather, fetch_forecast
from core.icons import get_icon_image, get_detail_icon
from core.storage import save_current_weather_to_csv, save_forecast_to_csv
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x720")
        self.root.configure(bg="#2E2E2E")  # Dark background

        self.city_var = tk.StringVar()

        # --- Centered Search Row ---
        self.input_container = ttk.Frame(root, style="InputRow.TFrame")
        self.input_container.pack(pady=10)

        self.input_frame = ttk.Frame(self.input_container)
        self.input_frame.pack(anchor='center')

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

        # Sharp styled tk.Button (not ttk)
        self.search_button = tk.Button(
            self.input_frame,
            text="Search",
            command=self.get_weather,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#5a5a5a",
            activebackground="#777777",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=5
        )
        self.search_button.pack(side="right")

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

        # --- Forecast area with horizontal scroll ---
        self.forecast_canvas = tk.Canvas(root, height=220, bg="#2E2E2E", highlightthickness=0, bd=0)
        self.scroll_x = ttk.Scrollbar(root, orient="horizontal", command=self.forecast_canvas.xview)
        self.forecast_canvas.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.pack(fill="x", side="bottom")
        self.forecast_canvas.pack(fill="x")

        self.forecast_frame = ttk.Frame(self.forecast_canvas, style="ForecastContainer.TFrame")
        self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")
        self.forecast_frame.bind("<Configure>", lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))

        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()

        style.configure("MainCard.TFrame", background="#3a3a3a", relief="solid", borderwidth=1)
        style.configure("CityTitle.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 18, "bold"))
        style.configure("Condition.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 11))
        style.configure("Detail.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10))

        style.configure("ForecastCard.TFrame", background="#3a3a3a", relief="solid", borderwidth=1)
        style.configure("ForecastLabel.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 9))
        style.configure("ForecastTitle.TLabel", background="#3a3a3a", foreground="white", font=("Segoe UI", 10, "bold"))

        style.configure("InputRow.TFrame", background="#2E2E2E")
        style.configure("ForecastContainer.TFrame", background="#2E2E2E")

    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            return

        weather = fetch_current_weather(city)
        forecast = fetch_forecast(city)

        if weather:
            temp = weather["main"]["temp"]
            description = weather["weather"][0]["description"].title()
            icon_code = weather["weather"][0]["icon"]

            self.city_label.config(text=city)
            self.temp_desc_label.config(text=f"{temp}°F, {description}")

            icon_image = get_icon_image(icon_code)
            if icon_image:
                self.icon_label.config(image=icon_image)
                self.icon_label.image = icon_image

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

        if forecast:
            save_forecast_to_csv(forecast)
            forecast_summary = self.process_forecast_data(forecast)
            self.clear_forecast_cards()

            for i, day in enumerate(forecast_summary):
                card = ttk.Frame(self.forecast_frame, padding=10, style="ForecastCard.TFrame", width=110)
                card.grid(row=0, column=i, padx=5, sticky="n")
                card.grid_propagate(False)

                dt = datetime.strptime(day["date"], "%Y-%m-%d")
                ttk.Label(card, text=dt.strftime("%a\n%b %d"), style="ForecastTitle.TLabel").pack(anchor="center")

                icon_image = get_icon_image(day["icon"])
                if icon_image:
                    icon_label = tk.Label(card, image=icon_image, bg="#3a3a3a")
                    icon_label.image = icon_image
                    icon_label.pack()

                ttk.Label(card, text=f"High: {day['high']}°F", style="ForecastLabel.TLabel").pack(anchor="center")
                ttk.Label(card, text=f"Low: {day['low']}°F", style="ForecastLabel.TLabel").pack(anchor="center")
                ttk.Label(card, text=day["desc"], style="ForecastLabel.TLabel", wraplength=90, justify="center").pack(anchor="center")
        else:
            self.clear_forecast_cards()

    def clear_forecast_cards(self):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

    def process_forecast_data(self, forecast_data):
        days = {}
        for item in forecast_data["list"]:
            date_str = item["dt_txt"].split()[0]
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"].title()
            icon = item["weather"][0]["icon"]

            if date_str not in days:
                days[date_str] = {"temps": [], "descs": [], "icons": []}

            days[date_str]["temps"].append(temp)
            days[date_str]["descs"].append(desc)
            days[date_str]["icons"].append(icon)

        forecast_summary = []
        for date_str in sorted(days.keys())[:5]:
            data = days[date_str]
            forecast_summary.append({
                "date": date_str,
                "high": round(max(data["temps"])),
                "low": round(min(data["temps"])),
                "desc": max(set(data["descs"]), key=data["descs"].count),
                "icon": max(set(data["icons"]), key=data["icons"].count)
            })

        return forecast_summary



