import tkinter as tk
from datetime import datetime
from core.icons import get_icon_image


def process_forecast_data(forecast_data, days=5):
    days_dict = {}
    for item in forecast_data["list"]:
        date_str = item["dt_txt"].split()[0]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].title()
        icon = item["weather"][0]["icon"]

        if date_str not in days_dict:
            days_dict[date_str] = {"temps": [], "descs": [], "icons": []}

        days_dict[date_str]["temps"].append(temp)
        days_dict[date_str]["descs"].append(desc)
        days_dict[date_str]["icons"].append(icon)

    forecast_summary = []
    for date_str in sorted(days_dict.keys())[:days]:
        data = days_dict[date_str]
        forecast_summary.append({
            "date": date_str,
            "high": round(max(data["temps"])),
            "low": round(min(data["temps"])),
            "desc": max(set(data["descs"]), key=data["descs"].count),
            "icon": max(set(data["icons"]), key=data["icons"].count)
        })

    return forecast_summary


# def show_forecast_popup(root, city, forecast_summary, days):
#     popup = tk.Toplevel(root)
#     popup.title(f"{days}-Day Forecast for {city}")
#     popup.configure(bg="#2E2E2E")
#     popup.geometry("1000x950")

#     title = tk.Label(popup, text=f"{days}-Day Forecast", font=("Segoe UI", 14, "bold"),
#                      fg="#FFA040", bg="#2E2E2E")
#     title.pack(pady=(20, 10))

#     content = tk.Frame(popup, bg="#2E2E2E")
#     content.pack(fill="both", expand=True, padx=20)

#     for i, day in enumerate(forecast_summary[:days]):
#         card = tk.Frame(content, bg="#3A3A3A", relief="raised", bd=1)
#         card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

#         try:
#             dt = datetime.strptime(day["date"], "%Y-%m-%d")
#             formatted_date = dt.strftime("%a, %b %d, %Y")
#         except:
#             formatted_date = day["date"]

#         tk.Label(card, text=formatted_date, font=("Segoe UI", 10, "bold"),
#                  fg="#FFA040", bg="#3A3A3A").pack(pady=(10, 0))

#         icon = get_icon_image(day["icon"])
#         if icon:
#             icon_label = tk.Label(card, image=icon, bg="#3A3A3A")
#             icon_label.image = icon
#             icon_label.pack(pady=5)

#         info = f"{day['desc']}\nHigh: {day['high']}°F • Low: {day['low']}°F"
#         tk.Label(card, text=info, font=("Segoe UI", 10),
#                  fg="white", bg="#3A3A3A").pack(pady=(0, 10))

#     chart_placeholder = tk.Frame(popup, bg="#2E2E2E", height=150)
#     chart_placeholder.pack(fill="both", expand=True, padx=20, pady=10)
#     tk.Label(chart_placeholder, text="(Chart goes here soon)", font=("Segoe UI", 10, "italic"),
#              fg="#888888", bg="#2E2E2E").pack()

#     tk.Button(
#         popup,
#         text="Close Forecast",
#         command=popup.destroy,
#         font=("Segoe UI", 11, "bold"),
#         bg="#FF6F00", fg="white",
#         relief="flat", padx=10, pady=6,
#         activebackground="#FFA040", activeforeground="black"
#     ).pack(pady=(10, 20))


def show_forecast_popup(root, city, forecast_summary, days, theme="dark"):
    # Define theme-based colors
    if theme == "dark":
        bg = "#2E2E2E"
        card_bg = "#3A3A3A"
        fg = "white"
        title_fg = "#FFA040"
        btn_bg = "#FF6F00"
        btn_active = "#FFA040"
        placeholder_fg = "#888888"
    else:
        bg = "#F9F6F3"
        card_bg = "#FFFFFF"
        fg = "#222222"
        title_fg = "#FF8C00"
        btn_bg = "#FFA94D"
        btn_active = "#FFB866"
        placeholder_fg = "#666666"

    popup = tk.Toplevel(root)
    popup.title(f"{days}-Day Forecast for {city}")
    popup.configure(bg=bg)
    popup.geometry("1000x950")

    # Title
    title = tk.Label(
        popup,
        text=f"{days}-Day Forecast",
        font=("Segoe UI", 14, "bold"),
        fg=title_fg,
        bg=bg
    )
    title.pack(pady=(20, 10))

    # Forecast container
    content = tk.Frame(popup, bg=bg)
    content.pack(fill="both", expand=True, padx=20)

    for i, day in enumerate(forecast_summary[:days]):
        card = tk.Frame(content, bg=card_bg, relief="raised", bd=1)
        card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        try:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            formatted_date = dt.strftime("%a, %b %d, %Y")
        except:
            formatted_date = day["date"]

        tk.Label(
            card,
            text=formatted_date,
            font=("Segoe UI", 10, "bold"),
            fg=title_fg,
            bg=card_bg
        ).pack(pady=(10, 0))

        icon = get_icon_image(day["icon"])
        if icon:
            icon_label = tk.Label(card, image=icon, bg=card_bg)
            icon_label.image = icon
            icon_label.pack(pady=5)

        info = f"{day['desc']}\nHigh: {day['high']}°F • Low: {day['low']}°F"
        tk.Label(
            card,
            text=info,
            font=("Segoe UI", 10),
            fg=fg,
            bg=card_bg
        ).pack(pady=(0, 10))

    # Chart placeholder
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