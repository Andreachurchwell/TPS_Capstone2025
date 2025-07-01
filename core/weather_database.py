import sqlite3
import os

# Create a path to /data/weather.db
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'weather.db')
DB_PATH = os.path.abspath(DB_PATH)

def init_db():
    """Create the forecast_data table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS forecast_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,  -- YYYY-MM-DD
            min_temp REAL,
            max_temp REAL,
            humidity INTEGER,
            wind_speed REAL,
            description TEXT,     -- e.g., Clear, Rain, Clouds
            icon_code TEXT,       -- for matching icons
            source_type TEXT      -- API or Predicted
        )
    ''')

    conn.commit()
    conn.close()

def save_forecast_to_db(city, forecast_list, source_type="API"):
    """
    Save a list of forecast entries to the forecast_data table.
    Each entry should be a dictionary with keys:
    date, min_temp, max_temp, humidity, wind_speed, description, icon_code
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for forecast in forecast_list:
        # Check if this forecast already exists
        c.execute('''
            SELECT id FROM forecast_data
            WHERE city = ? AND date = ? AND source_type = ?
        ''', (city, forecast['date'], source_type))

        if c.fetchone():
            continue  # Already saved

        # Insert the forecast entry
        c.execute('''
            INSERT INTO forecast_data 
            (city, date, min_temp, max_temp, humidity, wind_speed, description, icon_code, source_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            city,
            forecast['date'],
            forecast['min_temp'],
            forecast['max_temp'],
            forecast['humidity'],
            forecast['wind_speed'],
            forecast['description'],
            forecast['icon_code'],
            source_type
        ))

    conn.commit()
    conn.close()
