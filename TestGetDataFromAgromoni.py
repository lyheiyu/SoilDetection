{
    "id": "674f35aa23b9ed53d65e3d09",
    "geo_json": {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [30, 40],
                    [30.05, 40],
                    [30.05, 40.05],
                    [30, 40.05],
                    [30, 40]
                ]
            ]
        }
    },
    "name": "Test Polygon",
    "center": [30.025, 40.025],
    "area": 2372.342,
    "user_id": "674f2c6886ec340008b9359e",
    "created_at": 1733244330
}
import requests
from APIoperation import load_api_key

# 土壤数据 API URL
url = "http://api.agromonitoring.com/agro/1.0/soil"

# 使用多边形 ID 查询
params = {
    "polyid": "677e653fc46b9f856bdfb3f0",  # 替换为返回的 polygon_id
    "appid": load_api_key()  # 替换为您的 API Key
}

response = requests.get(url, params=params)

# 检查响应状态
if response.status_code == 200:
    print("Soil Data:", response.json())
else:
    print(f"Error: {response.status_code}")
    print("Response Content:", response.text)
