import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load CSV
df = pd.read_csv("ml/selmer_year.csv")

# Rename columns to match expected format
df = df.rename(columns={
    "precip": "precipitation",
    "max_wind_spd": "max_wind_speed"
})

df.dropna(inplace=True)

print(f"✅ Loaded {len(df)} Selmer rows")
print(df.head())

X = df[["min_temp",  "max_wind_speed"]]
y = df["max_temp"]

model = LinearRegression()
model.fit(X, y)

os.makedirs("ml", exist_ok=True)
joblib.dump(model, "ml/selmer_temp_model.pkl")

print("✅ New model trained and saved using full Selmer data")
