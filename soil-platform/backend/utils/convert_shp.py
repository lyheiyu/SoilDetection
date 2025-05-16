import geopandas as gpd
import os

def shp_to_geojson(shp_path):
    """
    将 .shp 文件转换为 GeoJSON 格式
    参数:
        shp_path: Shapefile 文件的路径（.shp）
    返回:
        生成的 GeoJSON 文件名（仅文件名，不含路径）
    """
    # 读取 .shp 文件
    gdf = gpd.read_file(shp_path)

    # 输出路径
    geojson_path = shp_path.replace(".shp", ".geojson")

    # 写入 GeoJSON 文件
    gdf.to_file(geojson_path, driver="GeoJSON")

    return os.path.basename(geojson_path)
