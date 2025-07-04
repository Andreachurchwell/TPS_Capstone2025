



import tkinter as tk
from datetime import datetime  # wanted to format my forecast dates
from core.icons import get_icon_image  # gets my weather icons
from features.forecast_charts import create_temp_chart

from features.custom_buttons import create_button



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
            # "high": round(max(data["temps"])),  # max temp
            # "low": round(min(data["temps"])),  # min temp
            "high": max(data["temps"]),  # leave raw Kelvin
            "low": min(data["temps"]),
            "desc": max(set(data["descs"]), key=data["descs"].count),  # most common description
            "icon": max(set(data["icons"]), key=data["icons"].count)  # most common icon code
        })

    return forecast_summary  # returns a list of daily summaries (1 a day)


# pops open a forecast window styled based on selected theme
def show_forecast_popup(root, city, forecast_summary, days, theme="dark", format_temp_func=None):
    # my set color scheme based on lite or dark mode
    if theme == "dark":
        bg = "#2E2E2E"         # main popup bg
        card_bg = "#3A3A3A"    # each forecast card bg
        fg = "white"           # regular text
        title_fg = "#FFA040"   # title color
        btn_bg = "#FF6F00"     # button bg
        btn_active = "#FFA040" # button hover color
    else:
        bg = "#F9F6F3"
        card_bg = "#FFFFFF"
        fg = "#222222"
        title_fg = "#FF8C00"
        btn_bg = "#FFA94D"
        btn_active = "#FFB866"

    # creates new popup window
    popup = tk.Toplevel(root)
    popup.title(f"{days}-Day Forecast for {city}")
    popup.configure(bg=bg)
    popup.geometry("1000x920")  # (you can shrink/adjust as you want)

    # Safe close binding
    def on_close():
        try:
            popup.destroy()
        except:
            pass
    popup.protocol("WM_DELETE_WINDOW", on_close)

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
    # content.pack(fill="both", expand=True, padx=20)
    content.pack(fill="x", padx=20, pady=10)

    # each forecast card
    for i, day in enumerate(forecast_summary[:days]):
        card = tk.Frame(content, bg=card_bg, relief="raised", bd=1)
        # card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")
        card.pack(side="left", padx=10, pady=10)

        try:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            formatted_date = dt.strftime("%a, %b %d, %Y")
        except:
            formatted_date = day["date"]

        # date label
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
            icon_label.image = icon  # keep a reference!
            icon_label.pack(pady=5)

        # weather info
        # info = f"{day['desc']}\nHigh: {day['high']}°F • Low: {day['low']}°F"
        if format_temp_func:
            high = format_temp_func(day['high'])
            low = format_temp_func(day['low'])
        else:
            high = f"{day['high']}°F"
            low = f"{day['low']}°F"

        info = f"{day['desc']}\nHigh: {high} • Low: {low}"
        tk.Label(
            card,
            text=info,
            font=("Segoe UI", 10),
            fg=fg,
            bg=card_bg
        ).pack(pady=(0, 10))

    # --- Chart container ---
    chart_frame = tk.Frame(popup, bg=bg)
    chart_frame.pack(fill="both", expand=True, padx=20, pady=(10,0))

    try:
        if forecast_summary and popup.winfo_exists():
            chart_canvas = create_temp_chart(forecast_summary, bg_color=bg, master=chart_frame, format_temp_func=format_temp_func)
            if chart_canvas:
                chart_canvas.get_tk_widget().pack(fill="both", expand=True)
    except Exception as e:
        print("Chart rendering failed:", e)

    close_btn = create_button(
        parent=popup,
        text="Close Forecast",
        command=popup.destroy,
        theme=theme  # uses dark/light mode color scheme
    )
    close_btn.pack(pady=(10, 30))


def process_extended_forecast_data(forecast, days=7):
    from datetime import datetime

    summary = []
    for day in forecast.get("list", [])[:days]:
        date = datetime.utcfromtimestamp(day["dt"]).strftime("%Y-%m-%d")
        high = day["temp"]["max"]
        low = day["temp"]["min"]
        desc = day["weather"][0]["description"].title()
        icon = day["weather"][0]["icon"]

        summary.append({
            "date": date,
            "high": high,
            "low": low,
            "desc": desc,
            "icon": icon
        })

    return summary
  