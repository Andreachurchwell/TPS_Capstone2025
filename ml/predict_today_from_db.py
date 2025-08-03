import sqlite3
import pandas as pd
import joblib
from datetime import date


def predict_max_temp():
    try:
        # Load trained model
        model = joblib.load("ml/selmer_temp_model.pkl")

        # Connect to DB
        conn = sqlite3.connect("data/weather.db")

        # Step 1: Try tomorrow's forecast
        query = """
        SELECT min_temp, wind_speed
        FROM forecast_data
        WHERE city = 'Selmer' AND date = DATE('now', '+1 day')
        LIMIT 1
        """
        row = pd.read_sql_query(query, conn)

        # Step 2: Fallback to today's forecast if needed
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

        # Match training format
        row = row.rename(columns={"wind_speed": "max_wind_speed"})

        print("[DEBUG] Forecast data used:", row.to_dict(orient="records"))

        X = row[["min_temp", "max_wind_speed"]]
        predicted_max = model.predict(X)[0]
        predicted_max = round(predicted_max, 1)

        # ✅ Load real accuracy
        accuracy = get_model_accuracy()
        if accuracy is None:
            print("[ML] Accuracy could not be loaded. Skipping prediction.")
            return None

        return predicted_max, accuracy

    except Exception as e:
        print(f"[ML ERROR] {e}")
        return None
    

def get_model_accuracy():
    try:
        with open("ml/model_accuracy.txt", "r") as f:
            score = float(f.read().strip())
            return round(score * 100, 1)  # Turn 0.7973 → 79.7%
    except Exception as e:
        print(f"[ML ERROR] Failed to load accuracy: {e}")
        return None