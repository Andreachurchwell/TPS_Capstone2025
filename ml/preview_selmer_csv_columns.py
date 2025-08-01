import pandas as pd

df = pd.read_csv("ml/selmer_year.csv")
print("📄 Columns in selmer_year.csv:")
print(df.columns.tolist())
