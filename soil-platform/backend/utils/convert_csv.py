import csv
import json
import os

def csv_to_geojson(csv_path):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        # 尝试自动识别字段名
        lat_key = next((h for h in headers if 'lat' in h.lower()), None)
        lon_key = next((h for h in headers if 'lon' in h.lower() or 'lng' in h.lower()), None)
        ph_key = next((h for h in headers if 'ph' == h.lower()), None)

        if not (lat_key and lon_key):
            raise ValueError("CSV lack of lat/lon")

        for row in reader:
            try:
                lat = float(row[lat_key])
                lon = float(row[lon_key])
                properties = {
                    "ph": float(row[ph_key]) if ph_key and row[ph_key] else None
                }
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": properties
                }
                geojson["features"].append(feature)
            except Exception as e:
                print(f"skip error: {e}")
                continue

    geojson_path = csv_path.replace(".csv", ".geojson")
    with open(geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False)

    return os.path.basename(geojson_path)
