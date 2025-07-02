# from core.api import fetch_current_weather, fetch_forecast

# def main():
#     city = input("Enter a city name: ")

#     # Current Weather
#     weather = fetch_current_weather(city)
#     if weather:
#         print(f"Current temperature in {city}: {weather['main']['temp']}°F")
#     else:
#         print("Could not get current weather data.")

#     # Forecast
#     forecast = fetch_forecast(city)
#     if forecast:
#         print("\n5-Day Forecast (every 3 hours):")
#         for item in forecast['list'][:5]:  # print first 5 data points only
#             dt = item['dt_txt']
#             temp = item['main']['temp']
#             description = item['weather'][0]['description']
#             print(f"{dt} | {temp}°F | {description}")
#     else:
#         print("Could not get forecast data.")


# if __name__ == "__main__":
#     main()

# import tkinter as tk
# from gui.main_window import MainWindow


# def main():
#     root = tk.Tk()
#     app = MainWindow(root)

#     root.mainloop()

# if __name__ == "__main__":
#     main()



# # testing splashscreen
# import tkinter as tk
# from gui.splash_screen import SplashScreen
# from gui.main_window import MainWindow
# from core.weather_database import init_db


# # my main entry point for launching the app
# def main():
#     init_db() #this sets up my db
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window initially

#     splash = SplashScreen(root)#creates and shows the ss
#     splash.wait_window()  # pauses here app wont move fwd until splash closes

#     root.deiconify()  # Show the main app window
#     MainWindow(root) #launches my weather dashboard

#     root.mainloop()#starts the event loop to keep app running

# # if __name__ == "__main__":
# #     main()

# if __name__ == "__main__":
#     try:
#         root = tk.Tk()
#         root.withdraw()

#         splash = SplashScreen(root)
#         splash.wait_window()

#         root.deiconify()
#         MainWindow(root)

#         root.mainloop()

#     except Exception:
#         pass  # ignore any last-second background errors



import tkinter as tk
from gui.splash_screen import SplashScreen
from gui.main_window import MainWindow
from core.weather_database import init_db

# Main entry point
def main():
    init_db()  # Set up database

    root = tk.Tk()
    root.withdraw()  # Hide main window during splash

    splash = SplashScreen(root)
    splash.wait_window()  # Wait until splash closes

    root.deiconify()  # Show main window
    MainWindow(root)

    root.mainloop()  # Start app loop

if __name__ == "__main__":
    main()


