import pandas as pd
import sqlite3
import os

DATA_DIR = "data"

def preview_csv(file_name):
    path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(path):
        print(f"\n📄 Previewing: {file_name}")
        try:
            df = pd.read_csv(path)
            print(f"✅ Rows: {len(df)} | Columns: {list(df.columns)}")
            print(df.head(3))
        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")
    else:
        print(f"❌ File not found: {file_name}")

def preview_db(db_name):
    db_path = os.path.join(DATA_DIR, db_name)
    if os.path.exists(db_path):
        print(f"\n🗃️ Previewing SQLite DB: {db_name}")
        try:
            conn = sqlite3.connect(db_path)
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
            print(f"📋 Tables: {tables['name'].tolist()}")
            for table_name in tables["name"]:
                print(f"\n🔍 Table: {table_name}")
                df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", conn)
                print(df.head())
            conn.close()
        except Exception as e:
            print(f"❌ Error reading DB: {e}")
    else:
        print(f"❌ Database not found: {db_name}")


if __name__ == "__main__":
    print("🔎 Scanning data folder for weather files...\n")

    preview_csv("current_weather.csv")
    preview_csv("current_weather_old.csv")
    preview_csv("forecast.csv")
    preview_db("weather.db")

    print("\n✅ Done!")