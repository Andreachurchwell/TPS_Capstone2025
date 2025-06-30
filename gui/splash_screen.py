import tkinter as tk
from PIL import Image, ImageTk
import os

class SplashScreen(tk.Toplevel):
    def __init__(self, root, duration=3000):
        super().__init__(root)

        self.duration = duration  # Time in ms
        self.configure(bg="#2e2e2e")
        self.overrideredirect(True)  # No window border

        # --- Center on screen ---
        window_width = 1000
        window_height = 950

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # --- Logo ---
        logo_path = os.path.join("assets", "icons", "snakebit_skies.png")
        logo_raw = Image.open(logo_path).resize((220, 220))
        self.logo_img = ImageTk.PhotoImage(logo_raw)

        self.logo_label = tk.Label(self, image=self.logo_img, bg="#1e1e1e")
        self.logo_label.pack(pady=(60, 10))

        self.app_name_label = tk.Label(
            self,
            text="Snakebit Skies",
            font=("Segoe UI", 28, "bold"),
            fg="#FFA040",
            bg="#2e2e2e"
        )
        self.app_name_label.pack()

        # --- Animated loading text ---
        self.loading_label = tk.Label(
            self,
            text="Loading weather data",
            font=("Segoe UI", 12),
            fg="#CCCCCC",
            bg="#2e2e2e"
        )
        self.loading_label.pack(pady=20)

        self.dot_count = 0
        self.animate_dots()

        # Auto-close after splash duration
        self.after(self.duration, self.destroy)

    def animate_dots(self):
        dots = "." * (self.dot_count % 4)
        self.loading_label.config(text=f"Loading weather data{dots}")
        self.dot_count += 1
        self.after(400, self.animate_dots)

