import pandas as pd

# Load the CSV file
df = pd.read_csv("ml/selmer_full_with_icons.csv")

# Show first 10 rows
print("First 10 rows:")
print(df.head(10))

# Show column names
print("\nColumns:")
print(df.columns.tolist())