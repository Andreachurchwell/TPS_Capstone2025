import joblib
import numpy as np

# Load your trained KNN model
knn = joblib.load("ml/knn_icon_model.pkl")

# Example input: min_temp, max_temp, wind_speed (replace with real forecast data later)
example_input = np.array([[65.0, 75.0, 5.0]])

# Predict icon
predicted_icon = knn.predict(example_input)[0]

print(f"Predicted weather icon: {predicted_icon}")