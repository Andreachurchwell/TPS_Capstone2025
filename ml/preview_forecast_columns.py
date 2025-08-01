import sqlite3
import pandas as pd

conn = sqlite3.connect("data/weather.db")
query = "SELECT * FROM forecast_data WHERE city = 'Selmer' LIMIT 1"
row = pd.read_sql_query(query, conn)
conn.close()

print("\n🧪 Column names in 'forecast_data':\n")
print(row.columns.tolist())