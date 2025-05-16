# import pandas as pd
# import geopandas as gpd
# import matplotlib.pyplot as plt
#
# # 文件路径
# shp_file_path = "Datasets/LUCAS-SOIL-2018 .shp"  # 替换为实际文件路径
# csv_file_path = "Datasets/LUCAS-SOIL-2018.csv"   # 替换为实际文件路径
#
# # 加载地理数据
# gdf = gpd.read_file(shp_file_path)
# print(gdf.columns)
#
# print(gdf.head())
# # ireland_data = gdf[gdf["NUTS_0"] == "IE"]
# # print(ireland_data.head())  # Preview filtered data
# ireland_data = gdf[
#     (gdf.geometry.x >= -11) & (gdf.geometry.x <= -5) &
#     (gdf.geometry.y >= 51) & (gdf.geometry.y <= 56)
# ]
#
# print(gdf.crs)
# print(ireland_data)
# # 加载土壤属性数据
# ireland_data = gdf.cx[-11:-5, 51:56]  # Ireland’s bounding box (longitude, latitude)
# print(ireland_data)
# csv_data = pd.read_csv(csv_file_path)
#
# # 确保列名一致（例如 `POINTID`）
# csv_data.rename(columns={"point_id_column_in_csv": "POINTID"}, inplace=True)
# print(csv_data.columns)
#
#
# print(csv_data.head())
#
# # 合并数据
#
# csv_data.rename(columns={"point_id_column_in_csv": "POINTID"}, inplace=True)
# merged_data = gdf.merge(csv_data, on="POINTID", how="inner")
# # merged_data = ireland_data.merge(csv_data, on="POINTID", how="inner")
# print(merged_data.head())
#
# # 绘制地图
# attribute_column = "pH_H2O"  # 替换为实际的列名
# fig, ax = plt.subplots(1, 1, figsize=(12, 8))
# merged_data.plot(column=attribute_column, cmap="viridis", legend=True, ax=ax)
#
# # 设置标题和标签
# plt.title("Soil pH Geographical Distribution", fontsize=15)
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.show()


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# File paths (replace with your actual file paths if different)
shp_file_path = "Datasets/LUCAS/LUCAS-SOIL-2018 .shp"
csv_file_path = "Datasets/LUCAS/LUCAS-SOIL-2018.csv"

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx  # For basemap


# Load geospatial data
gdf = gpd.read_file(shp_file_path)

# Check and set CRS to WGS 84 (EPSG:4326) for latitude/longitude
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4326)
else:
    gdf = gdf.to_crs(epsg=4326)

# Extract longitude and latitude for filtering
gdf["longitude"] = gdf.geometry.x
gdf["latitude"] = gdf.geometry.y

# Filter Ireland data using bounding box (approximate coordinates)
ireland_data = gdf[
    (gdf["longitude"] >= -11) & (gdf["longitude"] <= -5) &
    (gdf["latitude"] >= 51) & (gdf["latitude"] <= 56)
]

# Load soil attributes data
csv_data = pd.read_csv(csv_file_path)

# Ensure column names match before merging
csv_data.rename(columns={"point_id_column_in_csv": "POINTID"}, inplace=True)

# Merge Ireland's geospatial data with soil attributes
merged_data = ireland_data.merge(csv_data, on="POINTID", how="inner")

merged_data["N"] = pd.to_numeric(merged_data["N"], errors="coerce")

# Convert merged data to Web Mercator (EPSG:3857) for proper basemap overlay
merged_data = merged_data.to_crs(epsg=3857)

# Define pH column for visualization
# attribute_column = "pH_H2O"  # Adjust based on available data
attribute_column = "N"  # Adjust based on available data

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Normalize pH values for better visualization
min_pH, max_pH = merged_data[attribute_column].min(), merged_data[attribute_column].max()
print(min_pH, max_pH)
merged_data["size"] = 20 + 80 * (merged_data[attribute_column] - min_pH) / (max_pH - min_pH)  # Scale point sizes

# Plot data points with color based on pH values
sc = ax.scatter(
    merged_data.geometry.x,
    merged_data.geometry.y,
    c=merged_data[attribute_column],
    cmap="viridis",
    s=merged_data["size"],
    alpha=0.7,
    edgecolors="black"
)

# Add basemap from OpenStreetMap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Add color bar for pH scale
cbar = plt.colorbar(sc, ax=ax)
# cbar.set_label("Soil pH (H2O)")
cbar.set_label("Soil N)")

# Set plot labels
# ax.set_title("Soil pH Distribution in Ireland", fontsize=15)
ax.set_title("Soil N Distribution in Ireland", fontsize=15)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Show the plot
plt.show()

# Display a summary of the filtered dataset
print(f"Total soil data points in Ireland: {len(merged_data)}")
print(merged_data[[attribute_column, "size"]].head())
