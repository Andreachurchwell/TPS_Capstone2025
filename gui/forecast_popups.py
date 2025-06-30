import tkinter as tk
from datetime import datetime #wanted to format my forecast dates
from core.icons import get_icon_image #gets my weather icons

# cleans up forecast data from the api
def process_forecast_data(forecast_data, days=5):
    days_dict = {}
    # loops thru each 3 hour forecast entry
    for item in forecast_data["list"]:
        date_str = item["dt_txt"].split()[0]  # just yyy-mm-dd part
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].title()
        icon = item["weather"][0]["icon"]
# group all readings by date
        if date_str not in days_dict:
            days_dict[date_str] = {"temps": [], "descs": [], "icons": []}

        days_dict[date_str]["temps"].append(temp)
        days_dict[date_str]["descs"].append(desc)
        days_dict[date_str]["icons"].append(icon)

    forecast_summary = []

# goes thru grouped daily data and summarizes it
    for date_str in sorted(days_dict.keys())[:days]:
        data = days_dict[date_str]
        forecast_summary.append({
            "date": date_str,
            "high": round(max(data["temps"])), #max temp
            "low": round(min(data["temps"])), #min temp
            "desc": max(set(data["descs"]), key=data["descs"].count),#most common descripton
            "icon": max(set(data["icons"]), key=data["icons"].count)#most common icon code
        })

    return forecast_summary #returns a list of daily summaries(1 a day)

# ppops open a forecast window styled based on selected theme

def show_forecast_popup(root, city, forecast_summary, days, theme="dark"):

#    my set color scheme bases on lite or dark mode
    if theme == "dark":
        bg = "#2E2E2E" #main card
        card_bg = "#3A3A3A" #card bg
        fg = "white" #default text
        title_fg = "#FFA040" #title text color
        btn_bg = "#FF6F00" #btn bg
        btn_active = "#FFA040" #active btn color
        placeholder_fg = "#888888" #chart placeholder text
    else:
        bg = "#F9F6F3"
        card_bg = "#FFFFFF"
        fg = "#222222"
        title_fg = "#FF8C00"
        btn_bg = "#FFA94D"
        btn_active = "#FFB866"
        placeholder_fg = "#666666"
# creates new popup window
    popup = tk.Toplevel(root)
    popup.title(f"{days}-Day Forecast for {city}")
    popup.configure(bg=bg)
    popup.geometry("1000x950")

    # Title Label
    title = tk.Label(
        popup,
        text=f"{days}-Day Forecast",
        font=("Segoe UI", 14, "bold"),
        fg=title_fg,
        bg=bg
    )
    title.pack(pady=(20, 10))

    # main forecast area
    content = tk.Frame(popup, bg=bg)
    content.pack(fill="both", expand=True, padx=20)
# each forecast card
    for i, day in enumerate(forecast_summary[:days]):
        card = tk.Frame(content, bg=card_bg, relief="raised", bd=1)
        card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        try:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            formatted_date = dt.strftime("%a, %b %d, %Y") #pretty format mon, june 30, 2025
        except:
            formatted_date = day["date"]
# my date label
        tk.Label(
            card,
            text=formatted_date,
            font=("Segoe UI", 10, "bold"),
            fg=title_fg,
            bg=card_bg
        ).pack(pady=(10, 0))
# weather icon
        icon = get_icon_image(day["icon"])
        if icon:
            icon_label = tk.Label(card, image=icon, bg=card_bg)
            icon_label.image = icon
            icon_label.pack(pady=5)
# weather info text
        info = f"{day['desc']}\nHigh: {day['high']}°F • Low: {day['low']}°F"
        tk.Label(
            card,
            text=info,
            font=("Segoe UI", 10),
            fg=fg,
            bg=card_bg
        ).pack(pady=(0, 10))

    # placeholder for future charts
    chart_placeholder = tk.Frame(popup, bg=bg, height=150)
    chart_placeholder.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(
        chart_placeholder,
        text="(Chart goes here soon)",
        font=("Segoe UI", 10, "italic"),
        fg=placeholder_fg,
        bg=bg
    ).pack()

    # Close button
    tk.Button(
        popup,
        text="Close Forecast",
        command=popup.destroy,
        font=("Segoe UI", 11, "bold"),
        bg=btn_bg,
        fg="white",
        relief="flat",
        padx=10,
        pady=6,
        activebackground=btn_active,
        activeforeground="black"
    ).pack(pady=(10, 20))