import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load the CSV file
df = pd.read_csv("ml/selmer_full_with_icons.csv")

# 2. Select features and label
# Features: min_temp, max_temp, wind_speed
X = df[["min_temp", "max_temp", "wind_speed"]]

# Label: icon_code (weather condition icons)
y = df["icon_code"]

# 3. Split data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Create KNN classifier (you can tweak n_neighbors later)
knn = KNeighborsClassifier(n_neighbors=3)

# 5. Train the model
knn.fit(X_train, y_train)

# 6. Predict on the test set
y_pred = knn.predict(X_test)

# 7. Print accuracy and detailed report
print("Training accuracy:", knn.score(X_train, y_train))
print("Test accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification report:\n", classification_report(y_test, y_pred))

# 8. Save the trained model to file
joblib.dump(knn, "ml/knn_icon_model.pkl")
print("✅ KNN icon model trained and saved as 'ml/knn_icon_model.pkl'")