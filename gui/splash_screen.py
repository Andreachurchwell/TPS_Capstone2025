import tkinter as tk
from PIL import Image, ImageTk
import os


# this class makes a splash screen that appears before the main app
class SplashScreen(tk.Toplevel):
    def __init__(self, root, duration=3000):
        super().__init__(root)#inherits from toplevel which is like a temp window

        self.duration = duration  # Time in ms
        self.configure(bg="#2e2e2e")#bg color
        self.overrideredirect(True)  # No window border

        # --- Center on screen ---
        window_width = 1000
        window_height = 950

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
# calcs the center pos
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
# sets my splashscreen size and position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # --- Logo ---
        # loads and displays the logo img
        logo_path = os.path.join("assets", "icons", "snakebit_skies.png")
        logo_raw = Image.open(logo_path).resize((220, 220))
        self.logo_img = ImageTk.PhotoImage(logo_raw)

        self.logo_label = tk.Label(self, image=self.logo_img, bg="#1e1e1e")#lgo sits on darker box
        self.logo_label.pack(pady=(60, 10))#padding above and below
# my app name
        self.app_name_label = tk.Label(
            self,
            text="Snakebit Skies",
            font=("Segoe UI", 28, "bold"),
            fg="#FFA040",
            bg="#2e2e2e"
        )
        self.app_name_label.pack()

        # --- Animated loading label ---
        self.loading_label = tk.Label(
            self,
            text="Loading weather data",#base text(dots will animate)
            font=("Segoe UI", 12),
            fg="#CCCCCC",
            bg="#2e2e2e"
        )
        self.loading_label.pack(pady=20)

        self.dot_count = 0 #track how many dots show
        self.animate_dots()#starts my loop

        # Auto-close the splashscreen after duration ends
        self.after(self.duration, self.destroy)

 # Animates the "..." effect on the loading message
    def animate_dots(self):
        dots = "." * (self.dot_count % 4)#cycle between 0 and 3 dots
        self.loading_label.config(text=f"Loading weather data{dots}")
        self.dot_count += 1
        self.after(400, self.animate_dots)#updates every 400ms

