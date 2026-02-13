# TPS Capstone 2025 – Volunteer Weather 🌤️
Volunteer Weather is a sleek weather dashboard built with Python and Tkinter. It fetches real-time weather data and forecasts using the OpenWeatherMap API and presents it in a modern, user-friendly interface. Features include interactive maps, charts, and machine learning predictions — all styled with a bold theme that works in both dark and light modes.

## 🚀 Features
- 🌡️ Current weather by city (with icons and description)

- 📅 5-day, 7-day, 10-day, and 16-day forecast options

- 📍 Interactive map using TkinterMapView and RainViewer radar overlays

- 🧠 ML-powered temperature predictions (for Selmer, TN)

- 📊 Temperature trend chart with dark/light mode support

- 🔁 Toggle between Fahrenheit and Celsius

- 💾 Save weather data to CSV and SQLite

- 🧩 Modular code structure with reusable components

- 🌘 Splash screen with custom font and styling

- 🧑‍🤝‍🧑 Optional “Team Viewer” dashboard for shared data

## 🛠️ Getting Started
Prerequisites
- Python 3.8 or later
- A virtual environment (recommended)

An OpenWeatherMap API key

## 📦 Installation
Clone the repository:

```
git clone https://github.com/Andreachurchwell/TPS_Capstone2025.git
cd TPS_Capstone2025
```

### Create and activate a virtual environment:
PowerShell / Git Bash:
```
python -m venv venv
source venv/Scripts/activate
```
### Windows CMD:
```
venv\Scripts\activate
```
Install dependencies:
```
pip install -r requirements.txt
```
### Add your API key:
Create a .env file in the root directory with:
OPENWEATHER_API_KEY=your_api_key_here

## ▶️ Running the App
```
python app.py
```
## 🗂️ Project Structure

TPS_Capstone2025/
├── app.py                  # Entry point for the GUI
├── config.py               # API and environment settings
├── core/                   # API functions and data models
├── features/               # Custom components and tools
├── gui/                    # GUI layout and widgets
├── ml/                     # Machine learning files
├── team_7_Folder/          # Team Viewer dashboard
├── data/                   # Saved weather data (CSV + SQLite)
├── tests/                  # Test and preview scripts
├── docs/                   # Screenshots and extras
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed)
└── README.md


### 🙌 Acknowledgments
- OpenWeatherMap – For providing detailed current and forecast weather data

- RainViewer – For animated radar tiles used in the live weather map

- TkinterMapView – For the built-in, tile-based interactive map support

- Matplotlib – For creating trend charts

- Pillow (PIL) – For weather icon image handling

- Geopy – For coordinate-based location search and reverse geocoding

- CustomTkinter – For theming and modernizing the Tkinter GUI

- Justice Through Code and Columbia University – For the Tech Pathways program that supported and guided this project

- My TPS Team – For helping shape the Team Viewer feature with shared CSV data and feedback

- ChatGPT + AI Tools – For helping debug, brainstorm, and rewrite code

- GitHub – For version control, collaboration, and documentation

### 🧠 Notes
This project was built as a capstone for the TPS Summer 2025 program and is focused on clean architecture, real-world API integration, and visual polish. Features were added over time based on user feedback, testing, and exploratory learning.
