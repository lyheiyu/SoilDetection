import requests


url = "http://api.agromonitoring.com/agro/1.0/polygons"
params = {
    "appid": "dd61ba24bdb6abdc707992d7b6d20ee5",
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
