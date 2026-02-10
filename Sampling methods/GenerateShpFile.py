import geopandas as gpd

# 替换为你解压的本地路径
path = r"GADM/IRL_shape/gadm41_IRL_2.shp"

gdf = gpd.read_file(path)

# 筛选 Limerick
limerick = gdf[gdf["NAME_2"].str.contains("Limerick", case=False)].copy()

# 🌍 投影为等距坐标系（NAD83 / UTM zone 29N or Irish Grid）
# 可选投影：EPSG:2157 (IRENET95 / Irish Transverse Mercator)
limerick_proj = limerick.to_crs(epsg=2157)

# ✅ 正确计算中心点
limerick_proj["centroid"] = limerick_proj.geometry.centroid

# 转回 WGS84 用于导出
centroids_wgs84 = limerick_proj.set_geometry("centroid").to_crs(epsg=4326)

# 提取坐标
pt = centroids_wgs84.geometry.values[0]
print("中心点经度：", round(pt.x, 6))
print("中心点纬度：", round(pt.y, 6))

centroids_only = limerick_proj.set_geometry("centroid").to_crs(epsg=4326)
centroids_only = centroids_only.drop(columns=["geometry"])

# 现在只剩一个 geometry（centroid），可以安全导出
centroids_only.to_file("limerick/Limerick_Center.shp")
centroids_only["lon"] = centroids_only.geometry.x
centroids_only["lat"] = centroids_only.geometry.y
centroids_only[["lon", "lat"]].to_csv("limerick/Limerick_Center.csv", index=False)