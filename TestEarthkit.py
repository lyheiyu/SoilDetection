import os
import tempfile

from earthkit.geo import GeoKDTree

temp_dir = os.path.join("C:\\D\\temp")
os.makedirs(temp_dir, exist_ok=True)
tempfile.tempdir = temp_dir
from earthkit.regrid import interpolate
from earthkit.data import from_source
import earthkit.data as ekd

# data_file = r"C:\\D\\temp\\tmpk2jfewp6\\url-48a12069b8b9d38909c3a709c6c3bee9d51fef311fd94e587c95bd995acfb1f2.grib2"
# data = ekd.from_source("file", data_file)
#
# # Use your data as needed
# array = data.to_numpy()
# print(array)
#
# # Explicitly close and delete data object
#
#
# # # Create a stable directory
# # stable_temp_dir = r"C:\D\temp\earthkit_cache"
# # os.makedirs(stable_temp_dir, exist_ok=True)
# # os.environ["TMP"] = stable_temp_dir
# # os.environ["TEMP"] = stable_temp_dir
# #
# # # Then load data
# # data = ekd.from_source("file", data_file)
# # array = data.to_numpy()
# # print(array)
# #
# # del data
#
# # Define explicit paths for your temporary files
# # data_file = "C:\\D\\temp\\your_data.grib"
# #
# # # Use earthkit-data explicitly
# # data = ekd.from_source("file", data_file)
# # array = data.to_numpy()
#
# # After explicitly closing any file handles:
# # del data
# # Get HEALPix nested GRIB data containing two fields.
# ds = from_source(
#     "url",
#     "https://get.ecmwf.int/repository/test-data/earthkit-regrid/examples/H8_nested_multi.grib2")
#
# # the target grid is a global 5x5 degree regular latitude-longitude grid
# out_grid = {"grid": [5,5]}
#
# # perform interpolation for each field and add results
# # to a new fieldlist stored in memory
# r = interpolate(ds, out_grid=out_grid, method="linear")
#
# d = r.data()
# lat = d[0]
# lon = d[1]
# vals = d[2:]
# lat.shape, lon.shape, vals.shape
#
# import earthkit.plots
#
# figure = earthkit.plots.Figure(size=(9, 6), rows=1, columns=2)
# figure.add_map().plot(r[0])
# figure.add_map().plot(r[1])
# figure.coastlines()
# figure.subplot_titles()
# figure.legend()
# figure.gridlines(sharey=True)
# figure.show()
# ----------------------------

import os
import earthkit.data as ekd
from earthkit.regrid import interpolate
import earthkit.plots

# Optional: Define a stable temp directory if needed (uncomment if required)
# stable_temp_dir = r"C:\D\temp\earthkit_cache"
# os.makedirs(stable_temp_dir, exist_ok=True)
# os.environ["TMP"] = stable_temp_dir
# os.environ["TEMP"] = stable_temp_dir

# Load GRIB data from file
# data_file = 'data/936b16e7e8a786e8e45ac6667ed9320a.grib'
#
# import earthkit.data as ekd
#
# # reading only certain parts (byte ranges) from a single file
# ds = ekd.from_source("file", data_file)
#
# field_names = set(f.metadata("shortName") for f in ds)
#
# # 打印所有字段名
# print("variable name: shortName：")
# for name in sorted(field_names):
#     print(name)
# for f in ds:
#     print(f)
# reading only certain parts (byte ranges) from multiple files
# ds = ekd.from_source(
#     "file",
#     [
#         ("a.grib", (0, 150)),
#         ("b.grib", (240, 120)),
#         ("c.grib", None),
#         ("d.grib", [(240, 120), (720, 120)]),
#     ],
# )
# # data = ekd.from_source("file", data_file)
#
#
# # Convert data to NumPy array (if needed for further processing)
# array = data.to_numpy()
# print("Original data shape:", array.shape)
# print(data[0].metadata().keys())
# print(data[0].metadata("grid"))
# print(data[0].metadata("area"))
# print(data[0].metadata("shape"))
# # Get bounding box from input data
# area = [55.4, -10.5, 51.4, -5.5]
#
# # Define output grid with same area but coarser resolution
# out_grid = {
#     "grid": [0.5, 0.5],  # Try a more reasonable step size for a small region
#     "area": area
# }
#
# # Now interpolate
# from earthkit.regrid import interpolate
# r = interpolate(data, out_grid=out_grid, method="linear")
#
# # Define output grid (5x5 degree regular lat-lon grid)
#
#
# # Interpolate (regrid) data to the defined grid
#
# # Optional: access interpolated data if needed
# d = r.data()
# lat = d[0]
# lon = d[1]
# vals = d[2:]
# print("Interpolated lat shape:", lat.shape)
# print("Interpolated lon shape:", lon.shape)
# print("Interpolated values shape:", vals.shape)
#
# # Plot the regridded fields
# figure = earthkit.plots.Figure(size=(9, 6), rows=1, columns=2)
# figure.add_map().plot(r[0])
# figure.add_map().plot(r[1])
# figure.coastlines()
# figure.subplot_titles()
# figure.legend()
# figure.gridlines(sharey=True)
# figure.show()
#
# # Clean up resources
# # del data
# import earthkit.data as ekd
#
# # 替换成你的文件路径
data_file = "data/936b16e7e8a786e8e45ac6667ed9320a.grib"
# ds = ekd.from_source("file", data_file)
#
#
# variable_name = "swvl1"
# selected_fields = [f for f in ds if f.metadata("shortName") == variable_name]
#
# print(f"find {len(selected_fields)} number：{variable_name}")
# print("example:：")
# print(selected_fields[0].metadata())
# from earthkit.regrid import interpolate
#
# # 人工指定目标区域和网格（可以根据实际情况修改）
# out_grid = {
#     "grid": [0.5, 0.5],  # 纬度和经度分辨率
#     "area": [55.4, -10.5, 51.4, -5.5]  # [北, 西, 南, 东]，示例：爱尔兰附近区域
# }
#
# # 为节省内存，先处理前两个时间点
# import earthkit.data as ekd

# 直接在加载阶段就筛选出 swvl1
import numpy as np
import earthkit.data as ekd
import numpy as np
import matplotlib.pyplot as plt
# 区域范围 [北, 西, 南, 东]
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
data_file = "data/936b16e7e8a786e8e45ac6667ed9320a.grib"
swvl1_data = ekd.from_source("file", data_file, filter={"shortName": "swvl1"})
print("提取 swvl1 数据，请稍等……")
swvl1_array = np.stack([field.to_numpy() for field in swvl1_data])
print("数据 shape:", swvl1_array.shape)  # (105408, 17, 21)
# 构造经纬度网格
north, west, south, east = 55.4, -10.5, 51.4, -5.5
num_lat, num_lon = 17, 21

lats = np.linspace(north, south, num=num_lat)
lons = np.linspace(west, east, num=num_lon)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# 原始数据：swvl1 的第一个时间点
# data = swvl1_array[0]  # shape (17, 21)

# # 扁平化（用于插值）
# points = np.array([lat_grid.flatten(), lon_grid.flatten()]).T  # (N, 2)
# values = data.flatten()
# target_lat = np.linspace(north, south, 200)
# target_lon = np.linspace(west, east, 200)
# target_lon_grid, target_lat_grid = np.meshgrid(target_lon, target_lat)
#
# # 插值
# interp_data = griddata(points, values, (target_lat_grid, target_lon_grid), method='linear')
#
# plt.figure(figsize=(10, 6))
# ax = plt.axes(projection=ccrs.PlateCarree())
# cf = ax.pcolormesh(target_lon_grid, target_lat_grid, interp_data,
#                    cmap="YlGnBu", shading="auto", transform=ccrs.PlateCarree())
#
# ax.coastlines(resolution='10m')
# ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')
# ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
#
# plt.colorbar(cf, label="swvl1 soil temperature (m³/m³)")
# plt.title("swvl1 ")
# plt.tight_layout()
# plt.show()
from matplotlib.animation import FuncAnimation
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Geographic bounds (adjust if needed)
north, west, south, east = 55.4, -10.5, 51.4, -5.5
num_lat, num_lon = 17, 21

# Build lat/lon arrays
lats = np.linspace(north, south, num=num_lat)
lons = np.linspace(west, east, num=num_lon)
lon_grid, lat_grid = np.meshgrid(lons, lats)
points = np.array([lat_grid.flatten(), lon_grid.flatten()]).T

# Target interpolation grid
target_lat = np.linspace(north, south, 200)
target_lon = np.linspace(west, east, 200)
target_lon_grid, target_lat_grid = np.meshgrid(target_lon, target_lat)

# === Setup the figure ===
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
cf = ax.pcolormesh(target_lon_grid, target_lat_grid,
                   np.zeros_like(target_lat_grid),
                   cmap="YlGnBu", shading="auto", transform=ccrs.PlateCarree())

ax.coastlines(resolution='10m')
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')
ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
cbar = plt.colorbar(cf, ax=ax, orientation='vertical', label="swvl1 soil moisture (m³/m³)")
title = ax.set_title("")

# === Animation update function ===
def update(frame):
    data = swvl1_array[frame]  # shape (17, 21)
    values = data.flatten()
    interp_data = griddata(points, values, (target_lat_grid, target_lon_grid), method='linear')
    cf.set_array(interp_data.ravel())
    title.set_text(f"swvl1 Time Step {frame}")
    return cf, title

# === Create the animation ===
frames_to_plot = 200  # or len(swvl1_array)
anim = FuncAnimation(fig, update, frames=frames_to_plot, interval=100)

plt.tight_layout()
plt.show()