import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 加载 shapefile 数据
gdf = gpd.read_file("ESDB/SGDB_PTR.shp")

# 获取列名列表
columns = gdf.columns.tolist()
print(columns)
useful_columns = [
    'SOIL_', 'SOIL_ID', 'SMU', 'STU_DOM',
    'FAO90FU', 'FAO85FU', 'WRBFU',
    'FAO90LV1', 'FAO90LV2', 'FAO85LV1', 'FAO85LV2', 'FAO85LV3',
    'WRBLV1', 'WRBSPE1', 'WRBSPE2', 'WRBADJ1', 'WRBADJ2',
    'ZMAX', 'ZMIN',
    'AWC_TOP', 'AWC_SUB', 'EAWC_TOP', 'EAWC_SUB',
    'PD_TOP', 'PD_SUB', 'STR_TOP', 'STR_SUB',
    'CEC_TOP', 'CEC_SUB', 'BS_TOP', 'BS_SUB',
    'OC_TOP', 'MIN_TOP', 'MIN_SUB',
    'ERODI', 'TXEROD', 'CRUSTING', 'TXCRUST'
]
# select the useful columns from columns
columns = useful_columns

# 创建图像和轴
fig, ax = plt.subplots(figsize=(12, 8))

# 动画更新函数
def update(frame):
    column = columns[frame]
    ax.clear()
    gdf.plot(column=column, cmap='viridis', ax=ax)
    ax.set_title(f"Column: {column}", fontsize=16)

# 创建动画
ani = FuncAnimation(fig, update, frames=len(columns), repeat=True, interval=50)
# write a html to show the animation
# ani.save("soil_data_animation.html", fps=1, writer='html')  # 保存为 HTML
# write a mp4 to show the animation
# ani.save("soil_data_animation.mp4", fps=1, writer='ffmpeg')  # 保存为 MP4
# # 显示动画
# ani.save("soil_data_animation.mp4", fps=1, writer='ffmpeg')  # 保存为 MP4
# ani.save("soil_data_animation.gif", fps=1, writer='imagemagick')  # 保存为 GIF
plt.show()
