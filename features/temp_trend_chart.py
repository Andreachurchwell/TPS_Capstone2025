import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

def display_temperature_chart(parent, temps):
    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(5.5, 2.5), dpi=100)

    # Theme-aware colors
    mode = ctk.get_appearance_mode().lower()
    if mode == "dark":
        bg_color = "#1F1F1F"
        text_color = "#FFFFFF"
    else:
        bg_color = "#F2F2F2"
        text_color = "#000000"

    # Apply chart styling
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_color(text_color)

    # Plot the temperature line
    ax.plot(temps, color="#FF7E00", marker='o', linewidth=2.5)
    ax.set_title("Today’s Temperature Trend", color=text_color, fontsize=13)
    ax.set_xlabel("Hour", color=text_color)
    ax.set_ylabel("°F", color=text_color)
    ax.grid(True, linestyle='--', alpha=0.3)

    # Draw the chart inside your frame
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return canvas