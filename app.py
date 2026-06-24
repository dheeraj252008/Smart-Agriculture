import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Corporate Title Branding
st.set_page_config(page_title="Mahindra Agri Solutions - Dashboard", layout="wide")
st.title("🚜 Mahindra Agri Solutions Ltd.")
st.subheader("Capstone Project: Adoption of Remote Sensing for Groundwater & Crop Health")
st.markdown("---")

# Split the page layout into two columns for your two main project pillars
col_left, col_right = st.columns(2)

# ==========================================
# PILLAR 1: REMOTE SENSING FOR CROP HEALTH (LEFT)
# ==========================================
with col_left:
    st.header("🌿 Remote Sensing: Crop Health (NDVI)")
    st.write("Enter live satellite NDVI index values below to evaluate vegetation health:")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        val_a = st.number_input("Zone A NDVI", min_value=0.0, max_value=1.0, value=0.82, step=0.05)
        val_b = st.number_input("Zone B NDVI", min_value=0.0, max_value=1.0, value=0.65, step=0.05)
    with c_col2:
        val_c = st.number_input("Zone C NDVI", min_value=0.0, max_value=1.0, value=0.40, step=0.05)
        val_d = st.number_input("Zone D NDVI", min_value=0.0, max_value=1.0, value=0.75, step=0.05)

    crop_data = {
        "Mahindra Cluster": ["Zone A", "Zone B", "Zone C", "Zone D"],
        "Satellite NDVI Value": [val_a, val_b, val_c, val_d]
    }
    crop = pd.DataFrame(crop_data)
    st.dataframe(crop, use_container_width=True)

    # Chart Generation
    fig, ax = plt.subplots()
    colors = ['#1D8348' if x >= 0.7 else '#F4D03F' if x >= 0.5 else '#CB4335' for x in crop["Satellite NDVI Value"]]
    ax.bar(crop["Mahindra Cluster"], crop["Satellite NDVI Value"], color=colors)
    ax.set_ylabel("NDVI Strength Index")
    ax.set_ylim(0, 1.1)
    st.pyplot(fig)

    avg_ndvi = crop["Satellite NDVI Value"].mean()
    st.metric("Cluster Average NDVI Score", round(avg_ndvi, 2))


# ==========================================
# PILLAR 2: GROUNDWATER RESOURCE MONITORING (RIGHT)
# ==========================================
with col_right:
    st.header("💧 Remote Sensing: Groundwater Level")
    st.write("Adjust the sliders to simulate monitored seasonal aquifer changes:")
    
    w_jan = st.slider("Winter Level (Jan) - Meters", 0, 40, 18)
    w_mar = st.slider("Pre-Monsoon Level (Mar) - Meters", 0, 40, 16)
    w_may = st.slider("Peak Summer Level (May) - Meters", 0, 40, 12)
    w_aug = st.slider("Post-Monsoon Level (Aug) - Meters", 0, 40, 24)

    water_data = {
        "Monitored Season": ["January", "March", "May", "August"],
        "Water Table Depth": [w_jan, w_mar, w_may, w_aug]
    }
    water = pd.DataFrame(water_data)
    st.dataframe(water, use_container_width=True)

    # Chart Generation
    fig2, ax2 = plt.subplots()
    ax2.plot(water["Monitored Season"], water["Water Table Depth"], marker='o', color='#2E86C1', linewidth=2.5)
    ax2.set_ylabel("Groundwater Depth Metric")
    ax2.set_ylim(0, 45)
    st.pyplot(fig2)

    avg_water = water["Water Table Depth"].mean()
    st.metric("Average System Water Table", round(avg_water, 2))
