import sqlite3
import pandas as pd
import joblib
import numpy as np
from datetime import date

def predict_max_temp():
    try:
        # Load the trained model
        model = joblib.load("ml/selmer_temp_model.pkl")

        # Connect to the weather database
        conn = sqlite3.connect("data/weather.db")

        # Get today’s date
        today = date.today().strftime("%Y-%m-%d")

        # Query today's forecast for Selmer
        query = """
        SELECT min_temp, wind_speed
        FROM forecast_data
        WHERE city = 'Selmer' AND date = ?
        LIMIT 1
        """
        row = pd.read_sql_query(query, conn, params=[today])
        conn.close()

        if row.empty:
            return None  # no data available

        # ✅ Rename to match model's training column name
        row = row.rename(columns={"wind_speed": "max_wind_speed"})

        # Format data for prediction
        X = row[["min_temp", "max_wind_speed"]]
        predicted_max = model.predict(X)[0]

        return round(predicted_max, 1)

    except Exception as e:
        print(f"[ML ERROR] {e}")
        return None
    

def get_model_accuracy():
    try:
        with open("ml/model_accuracy.txt", "r") as f:
            score = float(f.read().strip())
            return round(score * 100, 1)  # e.g. 82.3%
    except Exception as e:
        print(f"[ML ERROR] Failed to load accuracy: {e}")
        return None

