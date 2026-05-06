import streamlit as st
import pandas as pd
import pydeck as pdk
import h3

st.set_page_config(layout="wide")

st.title("🚖 Ride Demand & Surge (H3 Hexagon View)")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/processed/predictions.csv")

# -----------------------------
# Convert lat/lng → H3 again (for safety)
# -----------------------------
df["h3_cell"] = df.apply(
    lambda row: h3.latlng_to_cell(row["lat"], row["lng"], 9),
    axis=1
)

# -----------------------------
# Aggregate per H3 cell
# -----------------------------
agg = df.groupby("h3_cell").agg({
    "demand_score": "mean",
    "surge_multiplier": "mean"
}).reset_index()

# -----------------------------
# Convert H3 → polygon boundary
# -----------------------------
def h3_to_polygon(h):
    boundary = h3.cell_to_boundary(h)
    return [[lng, lat] for lat, lng in boundary]

agg["polygon"] = agg["h3_cell"].apply(h3_to_polygon)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

min_demand = st.sidebar.slider("Min Demand", 0, 100, 0)
max_demand = st.sidebar.slider("Max Demand", 0, 100, 100)

filtered = agg[
    (agg["demand_score"] >= min_demand) &
    (agg["demand_score"] <= max_demand)
]

# -----------------------------
# Color mapping (based on demand)
# -----------------------------
def get_color(demand):
    if demand < 30:
        return [0, 255, 0, 100]   # green
    elif demand < 70:
        return [255, 165, 0, 120] # orange
    else:
        return [255, 0, 0, 160]   # red

filtered["color"] = filtered["demand_score"].apply(get_color)

# -----------------------------
# H3 Polygon Layer
# -----------------------------
layer = pdk.Layer(
    "PolygonLayer",
    data=filtered,
    get_polygon="polygon",
    get_fill_color="color",
    pickable=True,
    stroked=True,
    get_line_color=[255, 255, 255],
    line_width_min_pixels=1,
)

# -----------------------------
# View State
# -----------------------------
view_state = pdk.ViewState(
    latitude=40.7,
    longitude=-74.0,
    zoom=10,
    pitch=40,
)

# -----------------------------
# Tooltip
# -----------------------------
tooltip = {
    "html": "<b>Demand:</b> {demand_score}<br/><b>Surge:</b> {surge_multiplier}x",
    "style": {"color": "white"}
}

# -----------------------------
# Render Map
# -----------------------------
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
))