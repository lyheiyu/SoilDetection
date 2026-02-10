import geopandas as gpd
import numpy as np
import random
import os
from shapely.geometry import Polygon, Point

# Define a sample polygon (Limerick-style, replace with your real one)
coords = [(-8.63, 52.66), (-8.63, 52.67), (-8.61, 52.67), (-8.61, 52.66), (-8.63, 52.66)]
poly = Polygon(coords)
gdf_poly = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
gdf_proj = gdf_poly.to_crs(epsg=2157)  # Irish projected CRS
poly_proj = gdf_proj.geometry.values[0]

min_x, min_y, _, _ = poly_proj.bounds

def generate_grid_cells(polygon, size):
    minx, miny, maxx, maxy = polygon.bounds
    grid = []
    for x in np.arange(minx, maxx, size):
        for y in np.arange(miny, maxy, size):
            cell = Polygon([(x,y), (x+size,y), (x+size,y+size), (x,y+size)])
            if polygon.intersects(cell):
                clipped = polygon.intersection(cell)
                if clipped.area > 0:
                    grid.append(clipped)
    return grid

def sample_points_in_cell(cell, n):
    minx, miny, maxx, maxy = cell.bounds
    pts = []
    while len(pts) < n:
        x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        pt = Point(x, y)
        if cell.contains(pt):
            pts.append(pt)
    return pts

grid_cells = generate_grid_cells(poly_proj, 100)
sample_points = []
data = []

for idx, cell in enumerate(grid_cells):
    pts = sample_points_in_cell(cell, 3)
    for pt in pts:
        data.append({
            "cell_id": idx,
            "x_m": pt.x - min_x,
            "y_m": pt.y - min_y,
            "geometry": pt
        })

samples_gdf = gpd.GeoDataFrame(data, crs="EPSG:2157")
samples_gdf_wgs = samples_gdf.to_crs(epsg=4326)

# Export
os.makedirs("output", exist_ok=True)
samples_gdf_wgs.to_file("output/samples_relative_xy.geojson", driver="GeoJSON")
