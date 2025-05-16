from flask import Flask, render_template, request
import geopandas as gpd
import folium
import pandas as pd

app = Flask(__name__)

gdf = gpd.read_file("ESDB/SGDB_PTR.shp")
columns = gdf.columns.tolist()
default_column = 'OC_TOP'

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_column = request.form.get('column', default_column)

    if selected_column in gdf.columns:
        # 转换列为数值型，并处理缺失值
        gdf[selected_column] = pd.to_numeric(gdf[selected_column], errors='coerce')
        gdf[selected_column].fillna(0, inplace=True)

    # 创建地图
    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=8)

    # 添加 Choropleth 图层
    folium.Choropleth(
        geo_data=gdf,
        name='choropleth',
        data=gdf,
        columns=['OBJECTID', selected_column],
        key_on='feature.properties.OBJECTID',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=selected_column,
    ).add_to(m)

    # 返回地图部分的 HTML
    map_html = m._repr_html_()

    if request.method == 'POST':
        return map_html
    else:
        return render_template('index.html', map_html=map_html, columns=columns, selected_column=selected_column)
if __name__ == '__main__':
    app.run(debug=True)