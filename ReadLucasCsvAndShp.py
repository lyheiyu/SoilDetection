import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# 文件路径
shp_file_path = "Datasets/LUCAS-SOIL-2018 .shp"  # 替换为实际文件路径
csv_file_path = "Datasets/LUCAS-SOIL-2018.csv"   # 替换为实际文件路径

# 加载地理数据
gdf = gpd.read_file(shp_file_path)

# 加载土壤属性数据
csv_data = pd.read_csv(csv_file_path)

# 确保列名一致（例如 `POINTID`）
csv_data.rename(columns={"point_id_column_in_csv": "POINTID"}, inplace=True)

# 合并数据
merged_data = gdf.merge(csv_data, on="POINTID", how="inner")

# 绘制地图
attribute_column = "pH_H2O"  # 替换为实际的列名
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
merged_data.plot(column=attribute_column, cmap="viridis", legend=True, ax=ax)

# 设置标题和标签
plt.title("Soil pH Geographical Distribution", fontsize=15)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
