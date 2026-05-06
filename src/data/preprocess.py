import pandas as pd
import h3
import geopandas as gpd
import os


# -----------------------------------
# Load Data (CSV or PARQUET)
# -----------------------------------
def load_data(path):
    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    return pd.read_csv(path)


# -----------------------------------
# Load zone mapping from SHAPEFILE
# -----------------------------------
def load_zone_mapping():
    shp_path = "data/raw/taxi_zones.shp"

    if not os.path.exists(shp_path):
        print("⚠️ Shapefile not found → using fallback mapping")
        return None

    zones = gpd.read_file(shp_path)

    # Ensure correct coordinate system (WGS84)
    if zones.crs is not None and zones.crs.to_string() != "EPSG:4326":
        zones = zones.to_crs(epsg=4326)

    # Fix column name if needed
    if "LocationID" not in zones.columns:
        zones.columns = [col.lower() for col in zones.columns]
        if "locationid" in zones.columns:
            zones.rename(columns={"locationid": "LocationID"}, inplace=True)

    # Convert polygon → centroid
    zones["lat"] = zones.geometry.centroid.y
    zones["lng"] = zones.geometry.centroid.x

    return zones[["LocationID", "lat", "lng"]]


# -----------------------------------
# Preprocess
# -----------------------------------
def preprocess(df):

    # -----------------------------
    # 1. Datetime
    # -----------------------------
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

    # -----------------------------
    # 2. Time Features
    # -----------------------------
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['month'] = df['pickup_datetime'].dt.month

    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

    df['is_peak'] = df['hour'].apply(
        lambda x: 1 if (7 <= x <= 10 or 17 <= x <= 21) else 0
    )

    # -----------------------------
    # 3. GEO MAPPING
    # -----------------------------
    zone_map = load_zone_mapping()

    if zone_map is not None:
        df = df.merge(
            zone_map,
            left_on="PULocationID",
            right_on="LocationID",
            how="left"
        )

        df.rename(columns={
            "lat": "pickup_lat",
            "lng": "pickup_lng"
        }, inplace=True)

    else:
        # fallback (in case shapefile missing)
        lat_lng = df['PULocationID'].apply(
            lambda x: (40.6 + (x % 50)*0.005, -74.05 + (x % 50)*0.005)
        )
        df['pickup_lat'] = lat_lng.apply(lambda x: x[0])
        df['pickup_lng'] = lat_lng.apply(lambda x: x[1])

    # -----------------------------
    # 4. Clean
    # -----------------------------
    df = df.dropna(subset=['pickup_lat', 'pickup_lng'])

    # -----------------------------
    # 5. H3 Indexing (fast)
    # -----------------------------
    df['h3_cell'] = [
        h3.latlng_to_cell(lat, lng, 9)
        for lat, lng in zip(df['pickup_lat'], df['pickup_lng'])
    ]

    # -----------------------------
    # 6. Weather (placeholder)
    # -----------------------------
    df['weather_flag'] = 0

    return df