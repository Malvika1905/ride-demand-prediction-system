from src.data.preprocess import load_data, preprocess
from src.features.feature_engineering import create_features
from src.models.train_model import train
from src.pricing.pricing_engine import calculate_surge_multiplier

import pandas as pd
import numpy as np

# -----------------------------
# 1. Load NYC TLC dataset
# -----------------------------
df = load_data("data/raw/yellow_tripdata_sample.csv")

# -----------------------------
# 2. Preprocess
# -----------------------------
df = preprocess(df)

# -----------------------------
# 3. Create DEMAND (core logic)
# -----------------------------
# Demand = rides per (location + hour)
df['demand_score'] = df.groupby(['h3_cell', 'hour'])['pickup_datetime'].transform('count')

# Add randomness (real-world noise)
df['demand_score'] = df['demand_score'] + np.random.normal(0, 2, len(df))

# Remove negatives
df['demand_score'] = df['demand_score'].clip(lower=0)

# Normalize to 0–100
df['demand_score'] = (df['demand_score'] / df['demand_score'].max()) * 100

# -----------------------------
# DEBUG (before encoding)
# -----------------------------
print("Sample data (before encoding):")
print(df[['hour', 'h3_cell', 'demand_score']].head())

# -----------------------------
# 4. Feature Engineering
# -----------------------------
df, features = create_features(df)

X = df[features]
y = df['demand_score']

# -----------------------------
# 5. Train Model
# -----------------------------
model = train(X, y)

print("Training complete.")

# -----------------------------
# 6. Prediction
# -----------------------------
df['predicted_demand'] = model.predict(X)

# -----------------------------
# 7. Simulate Supply
# -----------------------------
# Random supply between 20–100 drivers
df['supply'] = np.random.randint(20, 100, size=len(df))

# -----------------------------
# 8. Surge Pricing
# -----------------------------
df['surge_multiplier'] = df.apply(
    lambda row: calculate_surge_multiplier(row['predicted_demand'], row['supply']),
    axis=1
)

# -----------------------------
# 9. Save Output for Dashboard
# -----------------------------
output_df = df[['pickup_lat', 'pickup_lng', 'predicted_demand', 'surge_multiplier']]

output_df.rename(columns={
    'pickup_lat': 'lat',
    'pickup_lng': 'lng',
    'predicted_demand': 'demand_score'
}, inplace=True)

output_df.to_csv("data/processed/predictions.csv", index=False)

print("Predictions saved to data/processed/predictions.csv")