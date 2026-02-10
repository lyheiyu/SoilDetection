import folium
import json

# Load GeoJSON
with open("output/samples_relative_xy.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Get center of the map
features = geojson_data['features']
center = features[0]['geometry']['coordinates'][::-1] if features else [52.66, -8.62]

# Create Leaflet map
m = folium.Map(location=center, zoom_start=16)

folium.GeoJson(
    geojson_data,
    name="Sampling Points",
    tooltip=folium.GeoJsonTooltip(fields=["cell_id", "x_m", "y_m"],
                                   aliases=["Cell ID", "X (m)", "Y (m)"])
).add_to(m)

m.save("output/sampling_map.html")
"✅ sampling_map.html has been created. You can open it in your browser."
