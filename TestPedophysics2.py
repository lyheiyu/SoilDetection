import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pedophysics.simulate import Soil
from pedophysics import predict

# Streamlit app title
st.title("Soil Property Prediction App")

# Sidebar inputs for soil properties
st.sidebar.header("Input Soil Properties")
bulk_ec = st.sidebar.text_input("Bulk EC (comma-separated)", "0.01, 0.02, 0.025, 0.03, 0.04")
clay = st.sidebar.text_input("Clay Content (comma-separated or single value)", "10, 12, 8, 15, 7")
porosity = st.sidebar.slider("Porosity", 0.0, 1.0, 0.4)
water_ec = st.sidebar.slider("Water EC", 0.0, 1.0, 0.5)

# Parse inputs
bulk_ec_values = [float(val.strip()) for val in bulk_ec.split(",")]
clay_values = [float(val.strip()) for val in clay.split(",")] if "," in clay else float(clay)

# Generate soil objects and predictions
soil_sample = Soil(bulk_ec=bulk_ec_values, clay=clay_values, porosity=porosity, water_ec=water_ec)
predicted_water = predict.Water(soil_sample)

# Display input values
st.write("### Input Values")
st.write(f"**Bulk EC:** {bulk_ec_values}")
st.write(f"**Clay Content:** {clay_values}")
st.write(f"**Porosity:** {porosity}")
st.write(f"**Water EC:** {water_ec}")

# Display predicted water content
st.write("### Predicted Water Content")
st.write(predicted_water)

# Create scatter plot
st.write("### Scatter Plot of Predicted Water Content")
fig, ax = plt.subplots(figsize=(10, 5.5))
ss = 150
ax.scatter(soil_sample.bulk_ec, predicted_water * 100, color='blue', alpha=0.8, s=ss, label="Predicted Water")
ax.set_xlim(0, max(bulk_ec_values) + 0.01)
ax.set_ylim(0, max(predicted_water) * 100 + 5)
ax.set_xlabel('Given Bulk EC [S/m]', fontsize=18)
ax.set_ylabel('Predicted Water [%]', fontsize=18)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=14)
ax.grid(True)
ax.legend(loc='upper right', fontsize=14)
st.pyplot(fig)

# Save plot
st.write("Plot saved as 'soil_water_prediction.png'.")
fig.savefig('soil_water_prediction.png')

st.write("### Notes")
st.markdown("""
- **Bulk EC:** The electrical conductivity of the bulk soil sample.
- **Clay Content:** The percentage of clay in the soil, which can be entered as a single value or a list.
- **Porosity:** The fraction of the soil volume that is occupied by pores.
- **Water EC:** The electrical conductivity of the water phase in the soil.

Adjust the input values in the sidebar to see how they affect the predicted water content and the scatter plot.
""")
