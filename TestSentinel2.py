import requests
import pandas as pd
# json = requests.get("https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=not (Collection/Name eq 'SENTINEL-2') and ContentDate/Start gt 2022-05-03T00:00:00.000Z and ContentDate/Start lt 2022-05-03T00:10:00.000Z&$orderby=ContentDate/Start&$top=100").json()
# df = pd.DataFrame.from_dict(json['value'])
#
# # Print only specific columns
# columns_to_print = ['Id', 'Name','S3Path','GeoFootprint']
# df[columns_to_print].head(3)
# print(df.head(3))
#
# json = requests.get('https://catalogue.dataspace.copernicus.eu/stac/collections/SENTINEL-2').json()
# print(json)

import requests

url = "https://catalogue.dataspace.copernicus.eu/stac/search"
params = {
    "collections": ["SENTINEL-2"],
    "datetime": "2024-01-01T00:00:00Z/2024-02-01T23:59:59Z",
    "bbox": [-10, 45, 10, 55],  # Bounding box (Europe example)
    "limit": 5
}

response = requests.post(url, json=params)
data = response.json()

for item in data["features"]:
    print("\nImage ID:", item["id"])
    print("Available assets:", item["assets"].keys())  # List available assets

    if "QUICKLOOK" in item["assets"]:
        print("Quicklook Image:", item["assets"]["QUICKLOOK"]["href"])  # Low-res preview

    if "PRODUCT" in item["assets"]:
        print("Full Sentinel-2 Data:", item["assets"]["PRODUCT"]["href"])  # Full dataset link


# df = pd.DataFrame.from_dict(json['value'])
# print(df.head())

import requests

# Replace with a Quicklook Image URL from your results
quicklook_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(92ef75c2-25c4-468e-aa38-774a60723427)/$value"
# quicklook_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products(3554d0cd-6c11-4f78-975f-9d2ca5b6f69a)/$value"
output_filename = "sentinel2_quicklook.jpg"

# Download the image
response = requests.get(quicklook_url, stream=True)
if response.status_code == 200:
    with open(output_filename, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"✅ Quicklook Image saved as {output_filename}")
else:
    print("❌ Failed to download Quicklook Image.")


import requests

# Copernicus Data Space username & password
USERNAME = "xinyu.yan@tus.ie"
PASSWORD = "Yxy19890723!"

full_data_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products(3554d0cd-6c11-4f78-975f-9d2ca5b6f69a)/$value"
output_filename = "sentinel2_full_data.zip"
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# Request with authentication
response = requests.post(TOKEN_URL, data={
    "grant_type": "password",
    "client_id": "cdse-public",
    "username": USERNAME,
    "password": PASSWORD
})


if response.status_code == 200:
    with open(output_filename, "wb") as file:
        for chunk in response.iter_content(1024 * 1024):  # Download in chunks
            file.write(chunk)
    print(f"✅ Full Sentinel-2 Data saved as {output_filename}")
else:
    print(f"❌ Failed to download. Status Code: {response.status_code}")

search_url = "https://catalogue.dataspace.copernicus.eu/stac/search"

params = {
    "collections": ["SENTINEL-2"],
    "datetime": "2024-01-01T00:00:00Z/2024-02-01T23:59:59Z",
    "bbox": [-10, 45, 10, 55],  # Bounding box (update for your area)
    "limit": 1
}

response = requests.post(search_url, json=params)
print(response.json())  # Check available download links


import zipfile
import os

# 设置文件路径（替换为你的下载路径）
zip_file = "sentinel2_full_data.zip"
output_folder = "sentinel2_extracted"

# 创建目标文件夹
os.makedirs(output_folder, exist_ok=True)

# 解压 ZIP 文件
with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(output_folder)

print(f"✅ 解压完成！数据已存放在: {output_folder}")
