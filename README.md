# 🚖 Ride Demand Prediction & Surge Pricing System

## Overview
This project predicts ride demand using spatio-temporal features and applies dynamic surge pricing based on supply-demand imbalance.

## Features
- Geospatial modeling using H3 hex indexing
- Demand prediction using Random Forest & XGBoost
- Dynamic surge pricing engine
- Interactive Streamlit dashboard (H3 hex map)

## Tech Stack
- Python, Pandas, NumPy
- Scikit-learn, XGBoost
- H3 (Uber)
- Geopandas (shapefile processing)
- Streamlit + PyDeck

## Pipeline
Raw Data → Preprocessing → H3 Indexing → Feature Engineering → ML Model → Prediction → Surge Pricing → Dashboard

## Run Locally
```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py