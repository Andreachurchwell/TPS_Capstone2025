import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def create_temp_chart(forecast_summary, bg_color="#2E2E2E", master=None,format_temp_fun=None):
#     """
#     Creates a Matplotlib line chart of high/low temps over the forecast period.
#     Returns a FigureCanvasTkAgg that can be packed into a Tkinter frame.
#     """
#     dates = [day["date"] for day in forecast_summary if day["high"] != "--"]
#     highs = [day["high"] for day in forecast_summary if day["high"] != "--"]
#     lows = [day["low"] for day in forecast_summary if day["low"] != "--"]

#     fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
#     ax.plot(dates, highs, label="High Temp", marker='o')
#     ax.plot(dates, lows, label="Low Temp", marker='o')

#     ax.set_title("Temperature Forecast", fontsize=10, color="white")
#     ax.set_ylabel("°F", color="white")
#     ax.set_xlabel("Date", color="white")
#     ax.tick_params(colors="white")
#     ax.legend(facecolor=bg_color, edgecolor="gray", fontsize=8)

#     fig.patch.set_facecolor(bg_color)
#     ax.set_facecolor(bg_color)

#     # # Turn into a canvas widget
#     # chart_canvas = FigureCanvasTkAgg(fig, master=None)
#     # return chart_canvas

#     return FigureCanvasTkAgg(fig, master=master)


# def create_temp_chart(forecast_summary, bg_color="#2E2E2E", master=None, format_temp_func=None):
#     dates = [day["date"] for day in forecast_summary]
#     highs = [day["high"] for day in forecast_summary]
#     lows = [day["low"] for day in forecast_summary]

#     # If we have a formatter, use it to convert Kelvin to F or C
#     if format_temp_func:
#         highs = [float(format_temp_func(temp).replace("°F", "").replace("°C", "")) for temp in highs]
#         lows = [float(format_temp_func(temp).replace("°F", "").replace("°C", "")) for temp in lows]
#         print("Formatter is working!")
#         print("Highs after formatting:", highs)
#         print("Lows after formatting:", lows)
#     fig, ax = plt.subplots()
#     fig.patch.set_facecolor(bg_color)
#     ax.set_facecolor(bg_color)

#     ax.plot(dates, highs, label="High", marker='o')
#     ax.plot(dates, lows, label="Low", marker='o')

#     ax.set_title("Temperature Trend")
#     ax.set_ylabel("Temperature")
#     ax.set_xlabel("Date")
#     ax.legend()

#     canvas = FigureCanvasTkAgg(fig, master=master)
#     return canvas

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def create_temp_chart(forecast_summary, bg_color="#2E2E2E", master=None, format_temp_func=None):
#     dates = []
#     highs = []
#     lows = []

#     for day in forecast_summary:
#         if day["high"] == "--" or day["low"] == "--":
#             continue  # Skip days with missing data

#         try:
#             high = float(format_temp_func(day["high"]).replace("°F", "").replace("°C", ""))
#             low = float(format_temp_func(day["low"]).replace("°F", "").replace("°C", ""))
#         except:
#             continue  # Skip if conversion fails

#         dates.append(day["date"])
#         highs.append(high)
#         lows.append(low)

#     fig, ax = plt.subplots()
#     fig.patch.set_facecolor(bg_color)
#     ax.set_facecolor(bg_color)

#     ax.plot(dates, highs, label="High", marker='o', color="#FFA040")  # bright orange
#     ax.plot(dates, lows, label="Low", marker='o', color="#00BFFF")   # deep sky blue

#     ax.set_title("Temperature Trend")
#     ax.set_ylabel("Temperature")
#     ax.set_xlabel("Date")
#     ax.legend()

#     ax.set_xticks(range(len(dates)))
#     ax.set_xticklabels(dates, rotation=30, ha="right", fontsize=8)

#     return FigureCanvasTkAgg(fig, master=master)




import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_temp_chart(forecast_summary, bg_color="#2E2E2E", master=None, format_temp_func=None):
    dates = []
    highs = []
    lows = []

    for day in forecast_summary:
        if day["high"] == "--" or day["low"] == "--":
            continue

        try:
            high = float(format_temp_func(day["high"]).replace("°F", "").replace("°C", ""))
            low = float(format_temp_func(day["low"]).replace("°F", "").replace("°C", ""))
        except:
            continue

        dates.append(day["date"])
        highs.append(high)
        lows.append(low)

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    x = range(len(dates))
    width = 0.35

    ax.bar([i - width/2 for i in x], highs, width, label='Highs', color="#FFA040")   # bright orange
    ax.bar([i + width/2 for i in x], lows, width, label='Lows', color="#00FFFF")    

    ax.set_title("Temperature Forecast", fontsize=12, color="white" if bg_color == "#2E2E2E" else "#222")
    ax.set_ylabel("Temp", color="white" if bg_color == "#2E2E2E" else "#222")
    ax.set_xlabel("Date", color="white" if bg_color == "#2E2E2E" else "#222")
    ax.set_xticks(list(x))
    ax.set_xticklabels(dates, rotation=30, ha="right", fontsize=8, color="white" if bg_color == "#2E2E2E" else "#222")
    ax.tick_params(axis='y', colors="white" if bg_color == "#2E2E2E" else "#222")
    ax.legend(facecolor=bg_color, edgecolor="gray", fontsize=8)

    return FigureCanvasTkAgg(fig, master=master)


