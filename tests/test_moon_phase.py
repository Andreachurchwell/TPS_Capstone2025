import customtkinter as ctk
import math

# Sample moon phase percentage (0 to 100%)
# For example: 0% = New Moon, 50% = Full Moon, 100% = New Moon again
moon_cycle_percent = 45  # You can change this

# Determine moon phase name from percentage
def get_moon_phase_name(percent):
    if percent <= 2 or percent >= 98:
        return "New Moon"
    elif 2 < percent <= 25:
        return "Waxing Crescent"
    elif 25 < percent <= 48:
        return "First Quarter"
    elif 48 < percent < 52:
        return "Full Moon"
    elif 52 <= percent <= 75:
        return "Waning Gibbous"
    elif 75 < percent <= 98:
        return "Last Quarter"
    else:
        return "Unknown Phase"

# Create main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Moon Phase Dial")
app.geometry("400x400")

# Create a canvas to draw the circular dial
canvas = ctk.CTkCanvas(app, width=300, height=300, bg="#1F1F1F", highlightthickness=0)
canvas.pack(pady=20)

# Draw the outer circle
canvas.create_oval(50, 50, 250, 250, outline="gray", width=4)

# Draw the arc representing current moon cycle progress
angle = (moon_cycle_percent / 100) * 360
canvas.create_arc(50, 50, 250, 250, start=90, extent=-angle, outline="white", width=8, style="arc")

# Draw the moon phase label
phase_name = get_moon_phase_name(moon_cycle_percent)
label = ctk.CTkLabel(app, text=f"{phase_name} ({moon_cycle_percent}%)", font=ctk.CTkFont(size=18, weight="bold"))
label.pack(pady=10)

# Run app
app.mainloop()
