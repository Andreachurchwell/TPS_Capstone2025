# TPS_Capstone2025
gui dashboard
# TPS Capstone 2025 - Weather App

## Project Overview

This project is a weather dashboard application built using Python and Tkinter. It fetches current weather and forecast data from the OpenWeatherMap API and displays it in a user-friendly GUI with maps, icons, and charts.

## Features

- Current weather lookup by city
- 5-day weather forecast with graphs
- Interactive map showing selected location
- Export weather data to CSV
- Modular architecture with core, GUI, and feature components

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment setup (recommended)
- OpenWeatherMap API key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Andreachurchwell/TPS_Capstone2025.git
   cd TPS_Capstone2025
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/Scripts/activate   # Windows PowerShell/Git Bash
# or
venv\Scripts\activate          # Windows CMD
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file in the project root and add your API key:

ini
Copy
Edit
OPENWEATHER_API_KEY=your_api_key_here
Running the App
Run the main script:

bash
Copy
Edit
python app.py
Project Structure
arduino
Copy
Edit
TPS_Capstone2025/
├── app.py
├── config.py
├── core/
├── features/
├── gui/
├── data/
├── docs/
├── tests/
├── requirements.txt
├── README.md
├── .env
└── venv/
