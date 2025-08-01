import sqlite3
import pandas as pd
import os

# Point to your DB file
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'weather.db'))
conn = sqlite3.connect(DB_PATH)

# List tables
print("\n✅ Tables in DB:")
print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn))

# Load and preview forecast data
df = pd.read_sql("SELECT * FROM forecast_data", conn)
print("\n✅ First 5 rows:")
print(df.head())

# Show unique cities and row count
print("\n✅ Cities recorded:", df['city'].unique())
print("✅ Total forecast rows:", len(df))

# Show latest entries
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print("\n✅ Most recent rows:")
print(df.sort_values("date", ascending=False).head(10))

conn.close()
