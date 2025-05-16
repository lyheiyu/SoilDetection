import requests

from APIoperation import load_api_key
url = "http://api.agromonitoring.com/agro/1.0/polygons"
params = {
    "appid": load_api_key(),
    "duplicated": "true"
}
data = {
    "name": "Test Polygon",
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
# [-8.64006, 52.66994], [-8.63956, 52.66994], [-8.63956, 52.66954]
                ]
            ]
        }
    }
}


response = requests.post(url, params=params, json=data)
if response.status_code == 200:
    polygon_id = response.json().get("id")
    print("Polygon ID:", polygon_id)
else:
    print(f"Error: {response.status_code}")
    print("Response Content:", response.text)
