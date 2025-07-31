# import pandas as pd

# # Load your CSV
# df = pd.read_csv("team_7_Folder/cleaned_weather_data_selmer.csv")
# print("[INFO] Loaded data:")
# print(df.head())

# # Check for missing values
# print("\n[INFO] Missing values per column:")
# print(df.isnull().sum())

# # Fill or drop missing values
# df["precip"].fillna(0, inplace=True)
# df["max_temp"].fillna(df["max_temp"].mean(), inplace=True)
# df["min_temp"].fillna(df["min_temp"].mean(), inplace=True)
# df["max_wind_spd"].fillna(df["max_wind_spd"].mean(), inplace=True)

# # Check again after filling
# print("\n[INFO] Missing values after cleaning:")
# print(df.isnull().sum())

# # Check for duplicates
# num_dupes = df.duplicated().sum()
# print(f"\n[INFO] Duplicate rows found: {num_dupes}")
# if num_dupes > 0:
#     df.drop_duplicates(inplace=True)
#     print("[INFO] Duplicates removed")

# # Make sure date is datetime and sort it
# df["date"] = pd.to_datetime(df["date"])
# df.sort_values("date", inplace=True)

# # Final check
# print("\n[INFO] Data types:")
# print(df.dtypes)

# print("\n[INFO] DataFrame shape after cleaning:", df.shape)




import pandas as pd

# Load the CSV
df = pd.read_csv("team_7_Folder/cleaned_weather_data_selmer.csv")

print("[INFO] Loaded data:")
print(df.head())

# Check for missing values
print("\n[INFO] Missing values per column:")
print(df.isnull().sum())

# Clean missing values (using safe syntax to avoid FutureWarning)
df["precip"] = df["precip"].fillna(0)
df["max_temp"] = df["max_temp"].fillna(df["max_temp"].mean())
df["min_temp"] = df["min_temp"].fillna(df["min_temp"].mean())
df["max_wind_spd"] = df["max_wind_spd"].fillna(df["max_wind_spd"].mean())

# Check again after filling
print("\n[INFO] Missing values after cleaning:")
print(df.isnull().sum())

# Drop duplicate rows if any
num_dupes = df.duplicated().sum()
print(f"\n[INFO] Duplicate rows found: {num_dupes}")
if num_dupes > 0:
    df = df.drop_duplicates()
    print("[INFO] Duplicates removed")

# Convert 'date' column to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Final type and shape check
print("\n[INFO] Data types:")
print(df.dtypes)
print("[INFO] DataFrame shape after cleaning:", df.shape)

# Save final cleaned file
df.to_csv("team_7_Folder/final_cleaned_weather_data_selmer.csv", index=False)
print("\n[SUCCESS] Saved final cleaned file as team_7_Folder/final_cleaned_weather_data_selmer.csv")
