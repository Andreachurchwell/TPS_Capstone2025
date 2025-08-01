import sqlite3
import pandas as pd
import joblib
import numpy as np
from datetime import date

# 🔹 Load trained model
model = joblib.load("ml/selmer_temp_model.pkl")

# 🔹 Connect to the weather database
conn = sqlite3.connect("data/weather.db")

# 🔹 Get today’s date
today = date.today().strftime("%Y-%m-%d")

# 🔹 Query today's forecast for Selmer
query = """
SELECT min_temp, wind_speed
FROM forecast_data
WHERE city = 'Selmer' AND date = ?
LIMIT 1
"""
row = pd.read_sql_query(query, conn, params=[today])
conn.close()

# 🔹 Predict if data exists
if row.empty:
    print("⚠️ No Selmer forecast data found for today.")
else:
    min_temp = row.loc[0, "min_temp"]
    wind_speed = row.loc[0, "wind_speed"]

    # Format data for prediction
    X = np.array([[min_temp, wind_speed]])
    predicted_max = model.predict(X)[0]

    print(f"📅 Date: {today}")
    print(f"📍 Selmer Forecast | min: {min_temp}, wind: {wind_speed}")
    print(f"🔮 Predicted Max Temp: {predicted_max:.1f}°F")