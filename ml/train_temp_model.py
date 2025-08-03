import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import joblib
import os

# 🔹 Load and prepare data
df = pd.read_csv("ml/selmer_year.csv")
df = df.rename(columns={
    "precip": "precipitation",
    "max_wind_spd": "max_wind_speed"
})
df.dropna(inplace=True)

print(f"✅ Loaded {len(df)} Selmer rows")
print(df.head())

# 🔹 Define features and target
X = df[["min_temp", "max_wind_speed"]]
y = df["max_temp"]

# 🔹 Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 🔹 Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 🔹 Show results in terminal
print("\n📊 Model Evaluation Metrics:")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²:", round(r2, 4))

# 🔹 Save model
os.makedirs("ml", exist_ok=True)
joblib.dump(model, "ml/selmer_temp_model.pkl")
print("✅ Model saved to ml/selmer_temp_model.pkl")

# 🔹 Save R² accuracy score to file
with open("ml/model_accuracy.txt", "w") as f:
    f.write(str(r2))
print("✅ Accuracy saved to ml/model_accuracy.txt")