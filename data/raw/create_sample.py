import pandas as pd

df = pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")

df = df.head(50000)  # keep only 50k rows

df.to_csv("data/raw/yellow_tripdata_sample.csv", index=False)

print("Sample dataset created!")