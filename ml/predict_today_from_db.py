import sqlite3
import pandas as pd
import joblib
from datetime import date

def predict_max_temp():
    try:
        # Load the trained model
        model = joblib.load("ml/selmer_temp_model.pkl")

        # Connect to the weather database
        conn = sqlite3.connect("data/weather.db")

        # 🧡 STEP 1: Try tomorrow's forecast first
        query = """
        SELECT min_temp, wind_speed
        FROM forecast_data
        WHERE city = 'Selmer' AND date = DATE('now', '+1 day')
        LIMIT 1
        """
        row = pd.read_sql_query(query, conn)

        # 🔁 STEP 2: If nothing found, fallback to today's forecast
        if row.empty:
            print("[DEBUG] No forecast found for tomorrow. Trying today instead.")
            fallback_query = """
            SELECT min_temp, wind_speed
            FROM forecast_data
            WHERE city = 'Selmer' AND date = DATE('now')
            LIMIT 1
            """
            row = pd.read_sql_query(fallback_query, conn)

        conn.close()

        if row.empty:
            print("[ML] No forecast data found for Selmer.")
            return None

        # ✅ Match training column names
        row = row.rename(columns={"wind_speed": "max_wind_speed"})

        # 🧪 Print inputs used for prediction
        print("[DEBUG] Forecast data used:", row.to_dict(orient="records"))

        # Format and predict
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
            return round(score * 100, 1)  # Example: 82.3%
    except Exception as e:
        print(f"[ML ERROR] Failed to load accuracy: {e}")
        return None