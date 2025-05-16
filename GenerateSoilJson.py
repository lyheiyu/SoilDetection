# import matplotlib.pyplot as plt
# from soilgrids import SoilGrids
# from pyproj import Transformer
#
#
# mollweide_wkt = """
# PROJCS["World_Mollweide",
#     GEOGCS["GCS_WGS_1984",
#         DATUM["WGS_1984",
#             SPHEROID["WGS_1984",6378137.0,298.257223563]],
#         PRIMEM["Greenwich",0.0],
#         UNIT["Degree",0.0174532925199433]],
#     PROJECTION["Mollweide"],
#     PARAMETER["False_Easting",0.0],
#     PARAMETER["False_Northing",0.0],
#     PARAMETER["Central_Meridian",0.0],
#     UNIT["Meter",1.0]]
# """
# transformer = Transformer.from_crs(mollweide_wkt, "EPSG:4326", always_xy=True)
# west, south = -1784000, 1356000
# east, north = -1140000, 1863000
# # lon_west, lat_south = transformer.transform(west, south)
# # lon_east, lat_north = transformer.transform(east, north)
#
# # get data from SoilGrids
# soil_grids = SoilGrids()
# data = soil_grids.get_coverage_data(
#     service_id="phh2o",
#     coverage_id="phh2o_0-5cm_mean",
#     west=west,
#     south=south,
#     east=east,
#     north=north,
#     crs="urn:ogc:def:crs:EPSG::152160",
#     output="test.tif",
# )
#
# # show metadata
# for key, value in soil_grids.metadata.items():
#     print(f"{key}: {value}")
#
#
# # plot data
# data.plot(figsize=(9, 5), vmin=0)
# plt.title("Mean pH between 0 and 5 cm soil depth in Senegal")
# plt.show()
import matplotlib.pyplot as plt
import numpy as np

from soilgrids import BmiSoilGrids

# from soilgrids import SoilGrids
# crsInfo=SoilGrids.get_coverage_info()
# print(crsInfo)
# initiate a data component
data_comp = BmiSoilGrids()
data_comp.initialize("config_file3.yaml")

# get variable info
var_name = data_comp.get_output_var_names()[0]
var_unit = data_comp.get_var_units(var_name)
var_location = data_comp.get_var_location(var_name)
var_type = data_comp.get_var_type(var_name)
var_grid = data_comp.get_var_grid(var_name)

print(f"{var_name=}")
print(f"{var_unit=}")
print(f"{var_location=}")
print(f"{var_type=}")
print(f"{var_grid=}")

# get variable grid info
grid_rank = data_comp.get_grid_rank(var_grid)

grid_size = data_comp.get_grid_size(var_grid)

grid_shape = np.empty(grid_rank, int)
data_comp.get_grid_shape(var_grid, grid_shape)

grid_spacing = np.empty(grid_rank)
data_comp.get_grid_spacing(var_grid, grid_spacing)

grid_origin = np.empty(grid_rank)
data_comp.get_grid_origin(var_grid, grid_origin)

print(f"{grid_rank=}")
print(f"{grid_size=}")
print(f"{grid_shape=}")
print(f"{grid_spacing=}")
print(f"{grid_origin=}")

# get variable data
data = np.empty(grid_size, var_type)
data_comp.get_value(var_name, data)
data_2D = data.reshape(grid_shape)

# get X, Y extent for plot
min_y, min_x = grid_origin
max_y = min_y + grid_spacing[0] * (grid_shape[0] - 1)
max_x = min_x + grid_spacing[1] * (grid_shape[1] - 1)
dy = grid_spacing[0] / 2
dx = grid_spacing[1] / 2
extent = [min_x - dx, max_x + dx, min_y - dy, max_y + dy]

# plot data
fig, ax = plt.subplots(1, 1, figsize=(9, 5))
im = ax.imshow(data_2D, extent=extent, vmin=0)
fig.colorbar(im)
plt.xlabel("X")
plt.ylabel("Y")
# plt.title("Mean pH between 0 and 5 cm soil depth in Senegal")
plt.title("Mean pH between 0 and 5 cm soil depth in Ireland")
# finalize data component
data_comp.finalize()
plt.show()


import rasterio
import numpy as np
import pandas as pd

# 读取 TIFF 文件
tif_file = "ireland_soil_pH.tif"
import rasterio
import numpy as np
import json
import pandas as pd

# 读取 SoilGrids 生成的 TIFF 文件
# tif_file = "ireland_soil_pH.tif"

# 解析 TIFF 文件
with rasterio.open(tif_file) as src:
    data = src.read(1)  # 读取第一个波段（pH 值数据）
    transform = src.transform  # 获取地理变换参数
    height, width = data.shape  # 获取行列数
    no_data_value = src.nodata  # 获取无效值

    # 计算每个像素的地理坐标
    rows, cols = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    xs, ys = rasterio.transform.xy(transform, rows, cols)

# **转换为 NumPy 数组**
xs = np.array(xs).flatten()  # 经纬度 X（经度）
ys = np.array(ys).flatten()  # 经纬度 Y（纬度）
data_flattened = data.flatten()  # pH 值数据

# **去除无效值**
valid_indices = data_flattened != no_data_value
filtered_xs = xs[valid_indices]
filtered_ys = ys[valid_indices]
filtered_ph = data_flattened[valid_indices]

# **转换为 DataFrame**
df = pd.DataFrame({
    "Longitude": filtered_xs,
    "Latitude": filtered_ys,
    "Soil_pH": filtered_ph/10
})

# **转换为 JSON 格式**
json_data = []
for _, row in df.iterrows():
    json_data.append({
        "latitude": row["Latitude"],
        "longitude": row["Longitude"],
        "ph_h2o": row["Soil_pH"]
    })

# **保存 JSON 文件**
output_json = "ireland_soil_ph_data.json"
with open(output_json, "w") as f:
    json.dump(json_data, f, indent=4)

print(f"✅ 生成 {len(json_data)} 条土壤 pH 数据，并保存到 {output_json}！")

