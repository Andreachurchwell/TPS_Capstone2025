import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_temp_chart(forecast_summary, bg_color="#2E2E2E", master=None):
    """
    Creates a Matplotlib line chart of high/low temps over the forecast period.
    Returns a FigureCanvasTkAgg that can be packed into a Tkinter frame.
    """
    dates = [day["date"] for day in forecast_summary if day["high"] != "--"]
    highs = [day["high"] for day in forecast_summary if day["high"] != "--"]
    lows = [day["low"] for day in forecast_summary if day["low"] != "--"]

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.plot(dates, highs, label="High Temp", marker='o')
    ax.plot(dates, lows, label="Low Temp", marker='o')

    ax.set_title("Temperature Forecast", fontsize=10, color="white")
    ax.set_ylabel("°F", color="white")
    ax.set_xlabel("Date", color="white")
    ax.tick_params(colors="white")
    ax.legend(facecolor=bg_color, edgecolor="gray", fontsize=8)

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # # Turn into a canvas widget
    # chart_canvas = FigureCanvasTkAgg(fig, master=None)
    # return chart_canvas

    return FigureCanvasTkAgg(fig, master=master)

