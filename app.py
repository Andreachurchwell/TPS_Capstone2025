

import tkinter as tk
from gui.splash_screen import SplashScreen
from gui.main_window import MainWindow
from core.weather_database import init_db
import customtkinter as ctk 


# Utility function to center a window on the screen
def center_window(window, width=1000, height=900):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Main entry point
def main():
    init_db()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = tk.Tk()
    root.withdraw()  # Hide the main window during splash

    # Show splash screen
    splash = SplashScreen(root)

    def launch_main():
        splash.destroy()                    # Remove splash
        root.deiconify()                    # Show main window
        center_window(root, 1000, 900)      # Center the main window
        MainWindow(root)                    # Launch your GUI on root

    # After splash duration, launch main window
    root.after(splash.duration, launch_main)

    root.mainloop()  # Start the main app loop

if __name__ == "__main__":
    main()

