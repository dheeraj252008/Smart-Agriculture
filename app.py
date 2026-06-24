import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Agriculture Monitoring System")
st.header("Crop Health Monitoring")
crop = pd.read_csv("crop_data.csv")
crop.columns = crop.columns.str.strip()
crop["NDVI"] = pd.to_numeric(crop["NDVI"], errors='coerce')
st.write(crop)

fig, ax = plt.subplots()
ax.bar(crop["Field"], crop["NDVI"])
ax.set_ylabel("NDVI")
st.pyplot(fig)

avg_ndvi = crop["NDVI"].mean()
st.metric("Average NDVI", round(avg_ndvi, 2))

st.header("Groundwater Monitoring")
water = pd.read_csv("groundwater_data.csv")
water.columns = water.columns.str.strip()
water["Water_Level"] = pd.to_numeric(water["Water_Level"], errors='coerce')
st.write(water)

fig2, ax2 = plt.subplots()
ax2.plot(water["Month"], water["Water_Level"])
ax2.set_ylabel("Water Level")
st.pyplot(fig2)

avg_water = water["Water_Level"].mean()
st.metric("Average Water Level", round(avg_water, 2))
