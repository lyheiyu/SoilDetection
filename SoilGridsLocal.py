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
# data_comp.initialize("config_file3.yaml")

data_comp.initialize("config_fileFrance.yaml")

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
plt.title("Mean pH between 0 and 5 cm soil depth")
# finalize data component
data_comp.finalize()
plt.show()


import rasterio
import numpy as np
import pandas as pd

# 读取 TIFF 文件
tif_file = "test3.tif"
with rasterio.open(tif_file) as src:
    data = src.read(1)  # 读取第一个波段
    transform = src.transform  # 获取地理变换参数
    height, width = data.shape  # 获取行数（纬度）和列数（经度）

    # 计算每个像素的地理坐标
    rows, cols = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    xs, ys = rasterio.transform.xy(transform, rows, cols)

# **将坐标转换为 NumPy 数组**
xs = np.array(xs).flatten()  # 经纬度 X（经度）
ys = np.array(ys).flatten()  # 经纬度 Y（纬度）
data_flattened = data.flatten()  # 土壤 pH 值

# **转换为 DataFrame**
df = pd.DataFrame({
    "Longitude": xs,  # 经度作为列
    "Latitude": ys,  # 纬度作为行
    "Soil_pH": data_flattened  # 土壤 pH 数据
})

# **转换为经纬度矩阵格式**
latitudes = np.unique(ys)  # 获取唯一纬度值（从南到北）
longitudes = np.unique(xs)  # 获取唯一经度值（从西到东）

# **创建经纬度 Grid 格式**
data_grid = data.reshape(len(latitudes), len(longitudes))

# **转换为 DataFrame**
df_grid = pd.DataFrame(data_grid, index=latitudes[::-1], columns=longitudes)  # 纬度倒序，使北方在上

# **保存 CSV**
csv_filename = "soil_pH_grid.csv"
df_grid.to_csv(csv_filename, index_label="Latitude")

# **返回文件路径**
csv_filename
