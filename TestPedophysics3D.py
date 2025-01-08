import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pedophysics.simulate import Soil
from pedophysics import predict
from matplotlib import cm
from matplotlib.colors import to_hex
import plotly.graph_objects as go
cmap=plt.get_cmap('viridis')
# Function to map water content to color
def get_color_by_water_content(water_content, min_val=0.0, max_val=1.0):
    """
    Maps water content (normalized between min_val and max_val) to a color.
    """
    normalized_value = (water_content - min_val) / (max_val - min_val)  # Normalize between 0 and 1
    colormap = cmap # Colormap from dry (red) to wet (blue)
    rgba_color = colormap(normalized_value)  # Get RGBA color
    hex_color = to_hex(rgba_color)  # Convert to HEX
    return hex_color

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

# Get the average predicted water content
average_water_content = np.nanmean(predicted_water)  # Use nanmean to handle any NaN values

# Map water content to color
cube_color = get_color_by_water_content(average_water_content, min_val=0.0, max_val=1.0)

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

# Add 3D cube for water content visualization
st.write("### 3D Cube Representation of Water Content")
st.write(f"**Average Water Content:** {average_water_content:.2f}")
st.write(f"**Cube Color (Based on Water Content):** {cube_color}")

# Create 3D cube
fig_3d = go.Figure()

# Define cube vertices
vertices = [
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Bottom face
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],  # Top face
]

# Define cube faces
faces = [
    [0, 1, 5, 4],  # Front
    [1, 2, 6, 5],  # Right
    [2, 3, 7, 6],  # Back
    [3, 0, 4, 7],  # Left
    [4, 5, 6, 7],  # Top
    [0, 1, 2, 3],  # Bottom
]

# Add cube to the figure
fig_3d.add_trace(go.Mesh3d(
    x=[v[0] for v in vertices],
    y=[v[1] for v in vertices],
    z=[v[2] for v in vertices],
    color=cube_color,
    opacity=0.8,
    i=[f[0] for f in faces],
    j=[f[1] for f in faces],
    k=[f[2] for f in faces],
    name="Water Content Cube",
))

# Customize the figure
fig_3d.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

# Render the 3D cube
st.plotly_chart(fig_3d)

# Notes section
st.write("### Notes")
st.markdown("""
- **Bulk EC:** The electrical conductivity of the bulk soil sample.
- **Clay Content:** The percentage of clay in the soil, which can be entered as a single value or a list.
- **Porosity:** The fraction of the soil volume that is occupied by pores.
- **Water EC:** The electrical conductivity of the water phase in the soil.

Adjust the input values in the sidebar to see how they affect the predicted water content, the scatter plot, and the 3D cube.
""")
