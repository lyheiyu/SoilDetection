import requests
import time
from APIoperation import load_api_key

API_KEY = load_api_key() # API Key
BASE_URL = "http://api.agromonitoring.com/agro/1.0"

def create_polygon():
    url = f"{BASE_URL}/polygons"
    params = {"appid": API_KEY, "duplicated": "true"}
    data = {
        "name": "Limerick Test Polygon",
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-8.64006, 52.66994],
                        [-8.63806, 52.66994],
                        [-8.63806, 52.66894],
                        [-8.64006, 52.66894],
                        [-8.64006, 52.66994]
                    ]
                ]
            }
        }
    }
    response = requests.post(url, params=params, json=data)
    if response.status_code == 201:
        polygon_id = response.json().get("id")
        print(f"Polygon created with ID: {polygon_id}")
        return polygon_id
    else:
        print(f"Error creating polygon: {response.status_code}")
        print(response.text)
        return None

def get_data(endpoint, polygon_id):
    url = f"{BASE_URL}/{endpoint}"
    params = {"polyid": polygon_id, "appid": API_KEY}
    print(f"Requesting {url} with params: {params}")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {endpoint} data: {response.status_code}")
        print(response.text)
        return None

def aggregate_data():
    # polygon_id = create_polygon()
    polygon_id = '677e653fc46b9f856bdfb3f0'
    if not polygon_id:
        print("Failed to create polygon. Exiting.")
        return

    soil_data = get_data("soil", polygon_id)
    weather_data = get_data("weather", polygon_id)
    historical_weather_data = get_data("weather/history", polygon_id)
    ndvi_data = get_data("image/search", polygon_id)

    aggregated_data = {
        "polygon_id": polygon_id,
        "soil_data": soil_data,
        "current_weather": weather_data,
        "historical_weather": historical_weather_data,
        "ndvi_data": ndvi_data
    }

    print("\nAggregated Data:")
    for key, value in aggregated_data.items():
        print(f"{key}: {value}")

    return aggregated_data

if __name__ == "__main__":
    aggregate_data()
