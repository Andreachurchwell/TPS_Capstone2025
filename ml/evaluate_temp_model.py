import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 🔹 Load your training data
df = pd.read_csv("ml/selmer_year.csv")  # <- make sure this is the same file you trained on

# 🔹 Features and target
X = df[["min_temp", "precip", "max_wind_spd"]]
y = df["max_temp"]

# 🔹 Split the data into train/test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train a fresh model on the training set
model = LinearRegression()
model.fit(X_train, y_train)

# 🔹 Predict on the test set
y_pred = model.predict(X_test)

# 🔹 Evaluate
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("📊 Temp Model Evaluation Results:")
print(f"• Mean Absolute Error (MAE): {mae:.2f}°F")
print(f"• Root Mean Squared Error (RMSE): {rmse:.2f}°F")
print(f"• R² Score: {r2:.2f}")