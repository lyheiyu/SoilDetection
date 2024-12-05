import requests
import time
# SoilGrids REST API URL
url = "https://rest.isric.org/soilgrids/v2.0/properties/query"

# 要查询的属性和深度
properties = ["soc", "phh2o", "bdod", "cec", "sand", "silt", "clay"]
depths = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]

# 查询位置
lon, lat = 5.0, 52.0  # 经度和纬度

# 获取数据
# 获取数据时添加延迟
for prop in properties:
    for depth in depths:
        params = {
            "lon": lon,
            "lat": lat,
            "property": prop,
            "depth": depth
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            layers = data.get("properties", {}).get("layers", [])
            for layer in layers:
                for d in layer["depths"]:
                    range_ = d["range"]
                    values = d["values"]
                    print(f"Property: {layer['name']}")
                    print(f"  Depth: {range_['top_depth']}cm - {range_['bottom_depth']}cm")
                    print(f"    Mean Value: {values.get('mean', 'N/A')}")
                    print(f"    Uncertainty: {values.get('uncertainty', 'N/A')}")
        else:
            print(f"Error fetching data for {prop} at depth {depth}: {response.status_code}")

        # 添加延迟，避免速率限制
        time.sleep(0.5)  # 延迟 1.5 秒
import geopandas as gpd
from shapely.geometry import Point

# 创建 GeoDataFrame
data_list = []
geometry = Point(lon, lat)

for prop in properties:
    for depth in depths:
        params = {
            "lon": lon,
            "lat": lat,
            "property": prop,
            "depth": depth
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            layers = data.get("properties", {}).get("layers", [])
            for layer in layers:
                for d in layer["depths"]:
                    range_ = d["range"]
                    values = d["values"]
                    data_list.append({
                        "property": layer["name"],
                        "top_depth": range_["top_depth"],
                        "bottom_depth": range_["bottom_depth"],
                        "mean_value": values.get("mean", None),
                        "uncertainty": values.get("uncertainty", None),
                        "geometry": geometry
                    })
import matplotlib.pyplot as plt
gdf = gpd.GeoDataFrame(data_list)
# output_file = "soil_data.geojson"
# gdf.to_file(output_file, driver="GeoJSON")
# print(f"GeoDataFrame saved as GeoJSON: {output_file}")
# print(gdf)
gdf.plot(column='mean_value', legend=True, cmap='viridis')
plt.title("Soil Data Visualization")
plt.show()