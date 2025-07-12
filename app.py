import tkinter as tk
from gui.splash_screen import SplashScreen
from gui.main_window import MainWindow
from core.weather_database import init_db
import customtkinter as ctk 


# Main entry point
def main():
    init_db()  # Set up database
    ctk.set_appearance_mode("dark")      # or "system" to auto-switch
    ctk.set_default_color_theme("dark-blue")
    root = tk.Tk()
    root.withdraw()  # Hide main window during splash

    splash = SplashScreen(root)
    splash.wait_window()  # Wait until splash closes

    root.deiconify()  # Show main window
    MainWindow(root)

    root.mainloop()  # Start app loop

if __name__ == "__main__":
    main()





