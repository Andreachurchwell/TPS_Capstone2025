import tkinter as tk
from PIL import Image, ImageTk


class SplashScreen(tk.Toplevel):
    def __init__(self, root, duration=3000):
        super().__init__(root)
        self.duration = duration

        self.configure(bg="#2E2E2E")  # Match dark theme
        self.overrideredirect(True)

        window_width = 900
        window_height = 900

        # Center on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Load and place logo
        # logo_path = "assets/icons/logo_splash.png"
        logo_path = "assets/icons/vw.png"
        logo_img = Image.open(logo_path).resize((650, 650))  # Adjust size if needed
        self.logo_tk = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(self, image=self.logo_tk, bg="#2E2E2E")
        logo_label.pack(expand=True)

  

        # Destroy splash after duration
        self.after(self.duration, self.destroy)







