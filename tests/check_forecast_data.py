import sqlite3
import pandas as pd
import os

# Point to the database from the test folder
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'weather.db'))

# Connect to DB
conn = sqlite3.connect(DB_PATH)

# Check available tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("\n✅ Tables in database:")
print(tables)

# Read forecast_data table
df = pd.read_sql("SELECT * FROM forecast_data", conn)
conn.close()

# Show preview
print("\n✅ First 5 rows:")
print(df.head())

print("\n✅ Cities recorded:")
print(df['city'].unique())

print("\n✅ Total forecast rows:", len(df))

# Try converting date field
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print("\n✅ Most recent forecasts:")
print(df.sort_values("date", ascending=False).head(10))