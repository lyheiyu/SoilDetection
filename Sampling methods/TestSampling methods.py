# from shapely.geometry import Polygon
# import geopandas as gpd
#
# # 假设在 Limerick 附近创建一个农田 polygon（单位是经纬度）
# # 实际可替换为你自己的农田 shapefile
# field_coords = [
#     (-8.63, 52.66),  # bottom left
#     (-8.63, 52.67),  # top left
#     (-8.61, 52.67),  # top right
#     (-8.61, 52.66),  # bottom right
#     (-8.63, 52.66)   # close polygon
# ]
# field_poly = Polygon(field_coords)
# field_gdf = gpd.GeoDataFrame(geometry=[field_poly], crs="EPSG:4326")
#
# field_proj = field_gdf.to_crs(epsg=2157)  # 爱尔兰国家投影系统
#
#
# import numpy as np
# from shapely.geometry import Point
#
# def generate_grid_within_polygon(polygon, spacing=100):
#     minx, miny, maxx, maxy = polygon.bounds
#     x_vals = np.arange(minx, maxx, spacing)
#     y_vals = np.arange(miny, maxy, spacing)
#     points = [Point(x, y) for x in x_vals for y in y_vals if polygon.contains(Point(x, y))]
#     return points
#
# # 取 polygon 对象
# poly_proj = field_proj.geometry.values[0]
# grid_points = generate_grid_within_polygon(poly_proj, spacing=100)  # 每100米一个点
#
# grid_gdf = gpd.GeoDataFrame(geometry=grid_points, crs=field_proj.crs)
#
#
# from sklearn.cluster import KMeans
#
# # 提取坐标
# coords = np.array([[pt.x, pt.y] for pt in grid_points])
#
# # 聚类采样（例如 10 个点）
# n_samples = 10
# kmeans = KMeans(n_clusters=n_samples, random_state=0).fit(coords)
#
# # 中心点作为样本
# centroids = [Point(x, y) for x, y in kmeans.cluster_centers_]
# sample_gdf = gpd.GeoDataFrame(geometry=centroids, crs=field_proj.crs)
#
#
#
# import matplotlib.pyplot as plt
#
# fig, ax = plt.subplots(figsize=(8, 8))
# field_proj.boundary.plot(ax=ax, color="black", label="Field Boundary")
# grid_gdf.plot(ax=ax, color="gray", markersize=2, alpha=0.4, label="Grid")
# sample_gdf.plot(ax=ax, color="red", markersize=50, label="Sample Points")
# plt.legend()
# plt.title("Spatial Coverage Sampling (KMeans)")
# plt.show()
#
# # 转回 WGS84 并导出为 CSV
# sample_wgs = sample_gdf.to_crs(epsg=4326)
# sample_wgs["lon"] = sample_wgs.geometry.x
# sample_wgs["lat"] = sample_wgs.geometry.y
# sample_wgs[["lon", "lat"]].to_csv("field_sample_points.csv", index=False)
# import geopandas as gpd
# import numpy as np
# import matplotlib.pyplot as plt
# from shapely.geometry import Polygon, Point
# import random
# import os
#
# # === 模拟 polygon（可换为你自己的 shapefile）===
# coords = [(-8.63, 52.66), (-8.63, 52.67), (-8.61, 52.67), (-8.61, 52.66), (-8.63, 52.66)]
# poly = Polygon(coords)
# gdf_poly = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
# gdf_proj = gdf_poly.to_crs(epsg=2157)  # 投影为米制坐标系
# poly_proj = gdf_proj.geometry.values[0]
#
# # === 网格参数 ===
# cell_size = 100  # 每个网格边长（单位：米）
# samples_per_cell = 3
#
# # === 步骤 1：生成网格 cell（polygon，不是点）===
# def generate_grid_cells(polygon, cell_size):
#     minx, miny, maxx, maxy = polygon.bounds
#     cells = []
#     for x0 in np.arange(minx, maxx, cell_size):
#         for y0 in np.arange(miny, maxy, cell_size):
#             x1, y1 = x0 + cell_size, y0 + cell_size
#             cell = Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
#             if polygon.intersects(cell):
#                 clipped = cell.intersection(polygon)
#                 if clipped.area > 0:
#                     cells.append(clipped)
#     return cells
#
# grid_cells = generate_grid_cells(poly_proj, cell_size)
# grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs=gdf_proj.crs)
#
# # === 步骤 2：每个 cell 内生成采样点（随机生成 N 个点）===
# def sample_points_within_cell(cell_poly, n):
#     minx, miny, maxx, maxy = cell_poly.bounds
#     points = []
#     attempts = 0
#     while len(points) < n and attempts < 100 * n:
#         x = random.uniform(minx, maxx)
#         y = random.uniform(miny, maxy)
#         pt = Point(x, y)
#         if cell_poly.contains(pt):
#             points.append(pt)
#         attempts += 1
#     return points
#
# all_samples = []
# for cell_id, cell in enumerate(grid_cells):
#     pts = sample_points_within_cell(cell, samples_per_cell)
#     all_samples.extend([(pt, cell_id) for pt in pts])
#
# samples_geom = [p[0] for p in all_samples]
# samples_cellid = [p[1] for p in all_samples]
# samples_gdf = gpd.GeoDataFrame({"cell_id": samples_cellid}, geometry=samples_geom, crs=gdf_proj.crs)
#
# # === 可视化 ===
# fig, ax = plt.subplots(figsize=(10, 10))
# gdf_proj.boundary.plot(ax=ax, color="black", linewidth=1)
# grid_gdf.boundary.plot(ax=ax, color="gray", linewidth=0.5)
# samples_gdf.plot(ax=ax, color="red", markersize=10)
# plt.title(f"{len(grid_gdf)} grid, {samples_per_cell} per cell ")
# plt.tight_layout()
# plt.show()
#
# # === 导出 ===
# samples_wgs = samples_gdf.to_crs(epsg=4326)
# samples_wgs["lon"] = samples_wgs.geometry.x
# samples_wgs["lat"] = samples_wgs.geometry.y
# samples_wgs[["cell_id", "lon", "lat"]].to_csv("output/spatial_coverage_sample.csv", index=False)
# samples_wgs.to_file("output/spatial_coverage_sample.shp")
#
# print(f"✅ 已生成 {len(samples_wgs)} 个采样点，覆盖 {len(grid_gdf)} 个网格")
# import geopandas as gpd
# import numpy as np
# import matplotlib.pyplot as plt
# from shapely.geometry import Polygon, Point
# import random
# import os
#
# # 模拟一个 polygon（可替换为你自己的 shp）
# coords = [(-8.63, 52.66), (-8.63, 52.67), (-8.61, 52.67), (-8.61, 52.66), (-8.63, 52.66)]
# poly = Polygon(coords)
# gdf_poly = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
# gdf_proj = gdf_poly.to_crs(epsg=2157)  # 使用爱尔兰国家平面坐标系
# poly_proj = gdf_proj.geometry.values[0]
#
# # 网格和采样参数
# cell_size = 100  # 每个格子的边长，单位米
# samples_per_cell = 3
#
# # 生成网格 polygon（带相对行列号）
# def generate_grid_cells_with_index(polygon, cell_size):
#     minx, miny, maxx, maxy = polygon.bounds
#     cells = []
#     row_id = 0
#     y_vals = np.arange(miny, maxy, cell_size)
#     x_vals = np.arange(minx, maxx, cell_size)
#     for y0 in y_vals:
#         col_id = 0
#         for x0 in x_vals:
#             x1, y1 = x0 + cell_size, y0 + cell_size
#             grid_cell = Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
#             if polygon.intersects(grid_cell):
#                 clipped = polygon.intersection(grid_cell)
#                 if clipped.area > 0:
#                     cells.append((clipped, row_id, col_id))
#             col_id += 1
#         row_id += 1
#     return cells
#
# grid_cells_info = generate_grid_cells_with_index(poly_proj, cell_size)
# grid_polys = [c[0] for c in grid_cells_info]
# grid_rows = [c[1] for c in grid_cells_info]
# grid_cols = [c[2] for c in grid_cells_info]
#
# grid_gdf = gpd.GeoDataFrame({
#     "row": grid_rows,
#     "col": grid_cols
# }, geometry=grid_polys, crs=gdf_proj.crs)
#
# # 在每个格子中随机生成 N 个采样点
# def sample_points_within_polygon(polygon, n):
#     minx, miny, maxx, maxy = polygon.bounds
#     points = []
#     attempts = 0
#     while len(points) < n and attempts < 100 * n:
#         x = random.uniform(minx, maxx)
#         y = random.uniform(miny, maxy)
#         pt = Point(x, y)
#         if polygon.contains(pt):
#             points.append(pt)
#         attempts += 1
#     return points
#
# sample_points = []
# sample_data = []
#
# for idx, row in grid_gdf.iterrows():
#     pts = sample_points_within_polygon(row.geometry, samples_per_cell)
#     for pt in pts:
#         sample_points.append(pt)
#         sample_data.append({
#             "cell_id": idx,
#             "row": row["row"],
#             "col": row["col"]
#         })
#
# samples_gdf = gpd.GeoDataFrame(sample_data, geometry=sample_points, crs=gdf_proj.crs)
#
# # 可视化
# fig, ax = plt.subplots(figsize=(8, 8))
# gdf_proj.boundary.plot(ax=ax, color="black")
# grid_gdf.boundary.plot(ax=ax, color="grey", linewidth=0.5)
# samples_gdf.plot(ax=ax, color="red", markersize=15)
# plt.title("Sampling Points with Relative Grid Coordinates")
# plt.tight_layout()
# plt.show()
#
# # 导出结果
# samples_wgs = samples_gdf.to_crs(epsg=4326)
# samples_wgs["lon"] = samples_wgs.geometry.x
# samples_wgs["lat"] = samples_wgs.geometry.y
#
# os.makedirs("output", exist_ok=True)
# samples_wgs[["cell_id", "row", "col", "lon", "lat"]].to_csv("output/samples_with_relative_grid.csv", index=False)
# samples_wgs.to_file("output/samples_with_relative_grid.shp")
#
# print(f"✅ 成功生成 {len(samples_wgs)} 个采样点，网格数: {len(grid_gdf)}")
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import random
import os

# Simulated polygon (replace with your own shapefile)
coords = [(-8.63, 52.66), (-8.63, 52.67), (-8.61, 52.67), (-8.61, 52.66), (-8.63, 52.66)]
poly = Polygon(coords)
gdf_poly = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
gdf_proj = gdf_poly.to_crs(epsg=2157)  # Irish Transverse Mercator

poly_proj = gdf_proj.geometry.values[0]
min_x, min_y, _, _ = poly_proj.bounds  # For relative coordinate calculation

# Grid and sampling parameters
cell_size = 100  # meters
samples_per_cell = 3

def generate_grid_cells_with_index(polygon, cell_size):
    minx, miny, maxx, maxy = polygon.bounds
    cells = []
    row_id = 0
    y_vals = np.arange(miny, maxy, cell_size)
    x_vals = np.arange(minx, maxx, cell_size)
    for y0 in y_vals:
        col_id = 0
        for x0 in x_vals:
            x1, y1 = x0 + cell_size, y0 + cell_size
            grid_cell = Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
            if polygon.intersects(grid_cell):
                clipped = polygon.intersection(grid_cell)
                if clipped.area > 0:
                    cells.append((clipped, row_id, col_id))
            col_id += 1
        row_id += 1
    return cells

grid_cells_info = generate_grid_cells_with_index(poly_proj, cell_size)
grid_polys = [c[0] for c in grid_cells_info]
grid_rows = [c[1] for c in grid_cells_info]
grid_cols = [c[2] for c in grid_cells_info]

grid_gdf = gpd.GeoDataFrame({
    "row": grid_rows,
    "col": grid_cols
}, geometry=grid_polys, crs=gdf_proj.crs)

def sample_points_within_polygon(polygon, n):
    minx, miny, maxx, maxy = polygon.bounds
    points = []
    attempts = 0
    while len(points) < n and attempts < 100 * n:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        pt = Point(x, y)
        if polygon.contains(pt):
            points.append(pt)
        attempts += 1
    return points

sample_points = []
sample_data = []

for idx, row in grid_gdf.iterrows():
    pts = sample_points_within_polygon(row.geometry, samples_per_cell)
    for pt in pts:
        sample_points.append(pt)
        sample_data.append({
            "cell_id": idx,
            "row": row["row"],
            "col": row["col"],
            "relative_x": pt.x - min_x,  # Relative X in meters
            "relative_y": pt.y - min_y   # Relative Y in meters
        })

samples_gdf = gpd.GeoDataFrame(sample_data, geometry=sample_points, crs=gdf_proj.crs)

# Visualize
fig, ax = plt.subplots(figsize=(8, 8))
gdf_proj.boundary.plot(ax=ax, color="black")
grid_gdf.boundary.plot(ax=ax, color="grey", linewidth=0.5)
samples_gdf.plot(ax=ax, color="red", markersize=15)
plt.title("Sampling Points with Relative (X, Y) Coordinates [in meters]")
plt.tight_layout()
plt.show()

# Export
samples_wgs = samples_gdf.to_crs(epsg=4326)
samples_wgs["lon"] = samples_wgs.geometry.x
samples_wgs["lat"] = samples_wgs.geometry.y

os.makedirs("output", exist_ok=True)
samples_wgs[["cell_id", "row", "col", "relative_x", "relative_y", "lon", "lat"]].to_csv("output/samples_relative_xy.csv", index=False)
samples_wgs.to_file("output/samples_relative_xy.shp")

print(f"✅ Generated {len(samples_wgs)} sampling points with relative coordinates (unit: meters)")

