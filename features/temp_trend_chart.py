import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
plt.rcParams["font.family"] = "Lucida Bright"
def display_temperature_chart(parent, temps, time_labels):
    # Large chart size, slim fonts
    fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=100)
    plt.subplots_adjust(bottom=0.2)  # add more space at the bottom

    # Theme-aware styling
    mode = ctk.get_appearance_mode().lower()
    if mode == "dark":
        bg_color = "#1F1F1F"
        text_color = "#FFFFFF"
    else:
        bg_color = "#F2F2F2"
        text_color = "#000000"

    # Background styling
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.tick_params(colors=text_color, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(text_color)

    # Orange line
    ax.plot(temps, color="#FF7E00", marker='o', linewidth=2.5)

    # Smaller, cleaner fonts
    ax.set_title("Today’s Temperature Trend", color=text_color, fontsize=11)
    ax.set_xlabel("Hour", color=text_color, fontsize=9)
    ax.set_ylabel("°F", color=text_color, fontsize=9)

    # X-axis hours
    ax.set_xticks(range(len(time_labels)))
    ax.set_xticklabels(time_labels, rotation=30, ha="center", fontsize=9)

    # Grid and layout
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout(pad=3)

    # Embed in GUI
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)  # ✅ This prevents memory buildup
    return canvas