import requests

# API 配置
BASE_URL = "http://api.agromonitoring.com/agro/1.0"
API_KEY = "dd61ba24bdb6abdc707992d7b6d20ee5"  # 替换为您的 API Key

# 获取多边形列表
url = f"{BASE_URL}/polygons"
params = {"appid": API_KEY}

response = requests.get(url, params=params)

if response.status_code == 200:
    polygons = response.json()
    if polygons:
        print("Existing Polygons:")
        for polygon in polygons:
            print(f"ID: {polygon['id']}, Name: {polygon.get('name', 'Unnamed')}")
    else:
        print("No polygons found.")
else:
    print(f"Error fetching polygons: {response.status_code}")
    print(response.text)
