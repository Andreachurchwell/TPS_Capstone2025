
This week I finally confirmed that I’m pulling the full 16-day forecast from OpenWeather, which was a huge win because I’d been unsure if I had access to that much data. I updated my forecast popup layout to handle longer ranges with horizontal scrolling, and my Matplotlib charts now show temp trends for each forecast range. I got good feedback from Afsana and Gulshan about possibly switching to scatter plots instead of line charts, and I plan to work more on improving those visuals during the break. I also spent time organizing my code better — breaking things into separate files, cleaning up my layout, and keeping things modular. I still plan to add a Fahrenheit to Celsius toggle, bind the Enter key to my search input, and maybe add autocomplete for city names. I didn’t touch machine learning yet because I want to get everything looking good first, but I do need to start seriously thinking about my data — especially how I’m going to use it if I want to predict future temperatures or conditions. That part’s coming soon.



🌦️ Project Name: Volunteer Weather
A bold, modern Python weather app built with Tkinter, pulling real-time forecasts and visual insights for any city.

🗂️ Project Structure (Folders & Files)
Folder/File	Purpose
core/	Handles API calls and weather database saving
features/	Extra features: charts, buttons, styling, export, etc.
gui/	GUI files like main_window.py, forecast_popups.py
assets/	Weather icons, logo, and visuals
app.py	Launches full app (main entry point)
.env	Stores API key safely
data/	Where CSVs and DB exports are stored

🧠 Key Features
✅ Current Weather Search
Type a city name and fetch current weather (via OpenWeather API)

Displays city, temp, description, icon

Includes sunrise/sunset time

Supports dark theme styling

✅ Forecasts (3/5/7/10/16-Day)
Buttons to view various forecast lengths

Pops up in a new window styled in dark/light mode

Shows date, icon, weather description, high/low temp



Uses forecast_popups.py

✅ Matplotlib Forecast Chart
Temp trends shown in a chart below the forecast cards

Background color matches dark/light theme

✅ City Map
TkinterMapView shows the searched city on an interactive map

Zooms to location

✅ Custom Theming
Orange, gray, black, and white color palette

Bold, unique font and dark/light switchable theme

Styled buttons and forecast cards using customtkinter

✅ CSV Export + Database
Current weather and forecast data can be saved to .csv

Data optionally saved into SQLite (or similar) DB

✅ Splash Screen
Logo appears on launch

Animated potential planned (e.g., spinning stars)

⚙️ Tech Stack
Language: Python

GUI: Tkinter (with customtkinter)

Charting: Matplotlib

API: OpenWeather (forecast, current)

Styling: Dark/light themes, hover effects

Storage: CSV, SQLite (through custom save functions)

Tools: dotenv for API key, PIL for icons

🧱 Architecture Philosophy
Modular → All code is split across clear folders

Clean GUI logic → Custom buttons used for consistency

Feature-rich but focused → Doesn’t try to do everything, just weather well

🛠️ Features in Progress or Coming Soon
Feature	Status
✅ 16-Day Forecast API	Working & confirmed! Needs full integration
⌛ F↔C Toggle	Planned
⌛ Enter key binding	Planned
⌛ Auto-complete city input	Planned
✅ Forecast popups modular	Already moved to forecast_popups.py
✅ Buttons class	Created and in use (clean UI)
✅ Charts scroll or scale with more days	Implemented!



📅 This Week’s Accomplishments (Capstone Progress)
✅ Confirmed and Switched to Real 16-Day Forecast
Tested https://api.openweathermap.org/data/2.5/forecast/daily

Confirmed: i'm actually getting full 16-day forecast data

Validated with real JSON results and debug checks

✅ Ready to drop this into full app logic (paused for now)

✅ Updated Forecast Popup Layout



✅ Matplotlib Chart Working in Popups
Shows temperature trends for selected forecast range

Fully styled background (dark/light)

Included in all popup windows

✅ Splash Screen & Logo Design Progress
Finalized splash screen layout

Brainstormed animated logo (e.g., spinning TN stars)

Reaffirmed “Volunteer Weather” branding idea

✅ Got Project Architecture Clean & Modular
Continued moving features into modular files (forecast_popups.py, custom_buttons.py, etc.)

Prevented code duplication

Clean layout now supports easy scaling

✅ Identified & Prioritized Next Features
F↔C toggle (planned)

Bind Enter key to input (planned)

Add city name autocomplete (planned)

Final styling polish for consistency across app (buttons, fonts, layout)

✅ Held Off on ML Temporarily
Discussed using Linear Regression for temp prediction and KNN for weather conditions

I decided to hold off until the GUI is fully settled (smart call)

✅ Participated in Office Hours, Breakouts, TA Prep














