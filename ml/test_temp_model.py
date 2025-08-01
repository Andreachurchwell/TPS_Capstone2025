import joblib
import numpy as np

# Load the model
model = joblib.load("ml/selmer_temp_model.pkl")

# 👇 Replace with real values later!
min_temp = 70
precip = 0.3
wind_speed = 3.5

# Predict max temp
X_test = np.array([[min_temp, precip, wind_speed]])
predicted_max = model.predict(X_test)[0]

print(f"\n🌡️ Predicted max temp: {predicted_max:.1f}°F\n")