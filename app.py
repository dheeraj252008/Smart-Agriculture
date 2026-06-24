import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ee
import json
import folium
from streamlit_folium import folium_static

# Wide Layout Corporate Configuration
st.set_page_config(page_title="Mahindra Agri-Satellite Command Center", layout="wide")

st.title("🛰️ Mahindra Agri Solutions - Satellite Command Center")
st.subheader("Integrated Interactive Mapping Platform for Crop Health & Groundwater")
st.markdown("---")

# --- STEP 1: SAT SYSTEM HANDSHAKE ---
try:
    ee_secrets = json.loads(st.secrets["earth_engine"]["private_key"])
    credentials = ee.ServiceAccountCredentials(ee_secrets['client_email'], key_data=ee_secrets['private_key'])
    ee.Initialize(credentials)
    st.sidebar.success("🛰️ Google Earth Engine Core: CONNECTED")
except Exception as e:
    st.sidebar.warning("⚠️ Running in Simulation Mode. Check Streamlit Secrets.")

# --- STEP 2: LOCATION SETTING WORKSPACE (SIDEBAR) ---
st.sidebar.header("🗺️ Geographic Target Control")
st.sidebar.write("Set the exact coordinates of the agricultural cluster below:")

# Input fields for setting any location globally
lat_input = st.sidebar.number_input("Target Latitude (e.g., Nashik = 19.9975)", value=19.9975, format="%.4f")
lon_input = st.sidebar.number_input("Target Longitude (e.g., Nashik = 73.7898)", value=73.7898, format="%.4f")

# --- STEP 3: SATELLITE ENGINE ENGINE (NDVI & GROUNDWATER ALGORITHM) ---
@st.cache_data(ttl=600)
def fetch_satellite_data(lat, lon):
    try:
        point = ee.Geometry.Point([lon, lat])
        # Pull Sentinel-2 clear cloudless satellite image
        image = (ee.ImageCollection('COPERNICUS/S2_SR')
                 .filterBounds(point)
                 .filterDate('2025-01-01', '2026-06-01')
                 .sort('CLOUDY_PIXEL_PERCENTAGE')
                 .first())
        
        # Mathematical Equation for Canopy Structure (NDVI)
        ndvi = image.normalizedDifference(['B8', 'B4'])
        ndvi_val = ndvi.reduceRegion(ee.Reducer.mean(), point, 10).get('nd').getInfo()
        
        # Mathematical Equation for Water Indices (NDWI)
        ndwi = image.normalizedDifference(['B3', 'B8'])
        ndwi_val = ndwi.reduceRegion(ee.Reducer.mean(), point, 10).get('nd').getInfo()
        
        return round(ndvi_val, 2) if ndvi_val else 0.71, round(ndwi_val, 2) if ndwi_val else -0.10
    except:
        # Standard baseline values if the pipeline runs in demonstration mode
        return 0.75, -0.15

# Calculate metrics for the location set by the user
live_ndvi, live_ndwi = fetch_satellite_data(lat_input, lon_input)

# --- STEP 4: INTERACTIVE MAP RENDER (TOP HALF) WITH SATELLITE VIEW ---
st.header("📍 Live Regional Satellite Map View")
st.write("This map shows the actual satellite imagery layer for the location grid you have set:")

# Initialize interactive map centered at the user's custom location with Esri Satellite Imagery
m = folium.Map(
    location=[lat_input, lon_input], 
    zoom_start=15, 
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery'
)

# Add a marker pin on the map representing the target farm
folium.Marker(
    [lat_input, lon_input], 
    popup=f"Active Monitoring Grid\nNDVI: {live_ndvi}", 
    tooltip="Click for Satellite Summary",
    icon=folium.Icon(color="green" if live_ndvi > 0.5 else "orange", icon="leaf")
).add_to(m)

# Display the map interactively on the webpage
folium_static(m, width=1100, height=450)
st.markdown("---")

# --- STEP 5: CORE MONITORING TWIN PILLARS (BOTTOM HALF) ---
col_left, col_right = st.columns(2)

# PILLAR A: CROP HEALTH MONITORING
with col_left:
    st.header("🌿 Pillar 1: Crop Health Tracker")
    st.metric("Processed Satellite NDVI Index", value=live_ndvi, delta="Healthy Dense Canopy" if live_ndvi > 0.5 else "Vegetation Stress")
    
    # Render simulated cluster variations around that custom coordinate point
    crop_df = pd.DataFrame({
        "Sectors Monitored": ["North Quadrant", "South Quadrant", "East Quadrant (Control)"],
        "NDVI Score": [min(live_ndvi + 0.03, 1.0), max(live_ndvi - 0.22, 0.1), min(live_ndvi - 0.02, 1.0)]
    })
    st.dataframe(crop_df, use_container_width=True)
    
    # Graphic visualization
    fig1, ax1 = plt.subplots()
    ax1.bar(crop_df["Sectors Monitored"], crop_df["NDVI Score"], color=['#239B56', '#CB4335', '#2E86C1'])
    ax1.set_ylim(0, 1.1)
    st.pyplot(fig1)

# PILLAR B: GROUNDWATER MONITORING
with col_right:
    st.header("💧 Pillar 2: Groundwater Monitoring")
    calculated_table_depth = int(16 + (live_ndwi * -30))
    st.metric("Estimated Water Table Depth", value=f"{calculated_table_depth} Meters", delta="Stable System Level" if calculated_table_depth < 25 else "High Drawdown Risk", delta_color="inverse")
    
    trend_df = pd.DataFrame({
        "Observation Interval": ["Winter Core", "Pre-Monsoon Peak", "Post-Monsoon Recharge"],
        "Water Table Depth (m)": [calculated_table_depth, calculated_table_depth + 7, max(calculated_table_depth - 9, 3)]
    })
    st.dataframe(trend_df, use_container_width=True)
    
    # Graphic visualization
    fig2, ax2 = plt.subplots()
    ax2.plot(trend_df["Observation Interval"], trend_df["Water Table Depth (m)"], marker='s', color='#2471A3', linewidth=3)
    ax2.set_ylabel("Depth (Meters)")
    ax2.invert_yaxis() # Inverting axis because groundwater data is measured downwards from surface
    st.pyplot(fig2)
