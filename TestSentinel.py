# import requests
# import pandas as pd
# from requests.auth import HTTPBasicAuth
#
# # username = 'xinyu.yan@tus.ie'
# # password = 'Yxy19890723!'
# #
# #
# # headers = {
# #     'User-Agent': 'Mozilla/5.0'
# # }
# #
# # response = requests.get(
# #     "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=startswith(Name,'S2A_MSIL2A_20230401T105621_N0509_R051_T31UGT_20230401T124938')",
# #     auth=HTTPBasicAuth(username, password),
# #     headers=headers
# # )
# #
# # print(response.status_code)
# # print(response.text)
#
# # json = requests.get("https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=not (Collection/Name eq 'SENTINEL-2') and ContentDate/Start gt 2022-05-03T00:00:00.000Z and ContentDate/Start lt 2022-05-03T00:10:00.000Z&$orderby=ContentDate/Start&$top=100").json()
# # df = pd.DataFrame.from_dict(json['value'])
# #
# # # Print only specific columns
# # columns_to_print = ['Id', 'Name','S3Path','GeoFootprint']
# #
# # print(df[columns_to_print].head(3))
# # # df[columns_to_print].head(3)
# # import requests
# # import json
# # # Step 1: 获取 Token
# # username = 'xinyu.yan@tus.ie'
# # password = 'Yxy19890723!'
# # token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
# #
# # payload = {
# #     'grant_type': 'password',
# #     'client_id': 'cdse-public',
# #     'username': username,
# #     'password': password
# # }
# #
# # token_data = requests.post(token_url, data=payload).json()
# # access_token = token_data['access_token']
# #
# # print("✅ Access Token obtained.")
# # with open("C:/D/projects/SoilDetection/SoilDetection/copernicus_token.json", "w") as f:
# #     json.dump(token_data, f)
# #
# # import requests
# #
# # # Make sure access_token is defined
# # import json
# #
# # with open("C:/D/projects/SoilDetection/SoilDetection/copernicus_token.json", "r") as f:
# #     token_data = json.load(f)
# #
# # access_token = token_data['access_token']
# # headers = {"Authorization": f"Bearer {access_token}"}
# #
# #
# # url = f"https://download.dataspace.copernicus.eu/odata/v1/Products(a5ab498a-7b2f-4043-ae2a-f95f457e7b3b)/$value"
# #
# # headers = {"Authorization": f"Bearer {access_token}"}
# #
# # # Create a session and update headers
# # session = requests.Session()
# # session.headers.update(headers)
# #
# # # Perform the GET request
# # response = session.get(url, stream=True)
# #
# # # Check if the request was successful
# # if response.status_code == 200:
# #     with open("product.zip", "wb") as file:
# #         for chunk in response.iter_content(chunk_size=8192):
# #             if chunk:  # filter out keep-alive new chunks
# #                 file.write(chunk)
# # else:
# #     print(f"Failed to download file. Status code: {response.status_code}")
# #     print(response.text)
#
# import requests
# import json
#
# #
# # import requests
# # import json
# # # Step 1: 获取 Token
# # username = 'xinyu.yan@tus.ie'
# # password = 'Yxy19890723!'
# # token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
# #
# # payload = {
# #     'grant_type': 'password',
# #     'client_id': 'cdse-public',
# #     'username': username,
# #     'password': password
# # }
# #
# # token_data = requests.post(token_url, data=payload).json()
# # access_token = token_data['access_token']
# #
# # headers = {"Authorization": f"Bearer {access_token}"}
# #
# # # ✅ 修复后的 URL（注意单引号！）
# # url = f"https://download.dataspace.copernicus.eu/odata/v1/Products(a5ab498a-7b2f-4043-ae2a-f95f457e7b3b)/$value"
# #
# # # 创建请求 session
# # session = requests.Session()
# # session.headers.update(headers)
# #
# # # 下载文件
# # response = session.get(url, stream=True)
# #
# # # 检查响应类型并保存
# # if response.status_code == 200 and 'application/zip' in response.headers.get('Content-Type', ''):
# #     with open("product.zip", "wb") as file:
# #         for chunk in response.iter_content(chunk_size=8192):
# #             if chunk:
# #                 file.write(chunk)
# #     print("✅ Download completed: product.zip")
# #
# #     # 验证文件头是否是 ZIP
# #     with open("product.zip", "rb") as f:
# #         signature = f.read(4)
# #         if signature == b'PK\x03\x04':
# #             print("✅ File is a valid ZIP")
# #         else:
# #             print("❌ Not a valid ZIP: incorrect file header")
# # else:
# #     print(f"❌ Download failed: {response.status_code}")
# #     print(response.text[:500])
# import requests
# from datetime import datetime, timedelta
#
# # Step 1: 获取令牌
# token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
# payload = {
#     'grant_type': 'password',
#     'client_id': 'cdse-public',
#     'username': 'xinyu.yan@tus.ie',
#     'password': 'Yxy19890723!'
# }
# token_data = requests.post(token_url, data=payload).json()
# access_token = token_data['access_token']
# print("✅ 成功获取访问令牌。")
#
# # Step 2: 查询 Athlone 附近产品（使用 MGRS T29UNV）
# headers = {"Authorization": f"Bearer {access_token}"}
#
# # 时间范围（过去 30 天）
# end_date = datetime.utcnow()
# start_date = end_date - timedelta(days=30)
#
# query_url = (
#     "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
#     f"?$filter=contains(Name,'T29UNV') and contains(Name,'MSIL2A') and "
#     f"ContentDate/Start gt {start_date.isoformat()}Z and ContentDate/Start lt {end_date.isoformat()}Z"
#     "&$orderby=ContentDate/Start desc&$top=3"
# )
#
# response = requests.get(query_url, headers=headers)
# productIds = []
# if response.status_code == 200:
#     data = response.json().get("value", [])
#     if not data:
#         print("⚠️ 没有找到符合条件的产品")
#     else:
#         print("✅ 找到产品如下：")
#         for product in data:
#             productIds.append(product["Id"])
#             print("📦 产品名称:", product["Name"])
#             print("🆔 产品ID:", product["Id"])
#             print("🕒 时间:", product["ContentDate"]["Start"])
#             print("-" * 40)
# else:
#     print(f"❌ 查询失败，状态码: {response.status_code}")
#     print(response.text)
# #
# # import requests
# # import os
# #
# # # 上一段代码中的 productIds 列表
# # # （确保它是在查询成功后填充的）
# # # productIds = [
# # #     # 示例，如果你已经动态生成这个列表，可省略此行
# # #     # "eb1fe961-0b2d-4e4f-8d21-8c0605255240",
# # #     # ...
# # # ]
# print(productIds)
# # import requests
# #
# # product_id = "eb1fe961-0b2d-4e4f-8d21-8c0605255240"
# #
# # headers = {
# #     "Authorization": f"Bearer {access_token}"
# # }
# #
# # url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$zip"
# #
# # with requests.get(url, headers=headers, stream=True) as r:
# #     if r.status_code == 200:
# #         with open(f"{product_id}.zip", "wb") as f:
# #             for chunk in r.iter_content(chunk_size=8192):
# #                 f.write(chunk)
# #         print("✅ 下载完成")
# #     else:
# #         print(f"❌ 下载失败，状态码: {r.status_code}")
# #         print(r.text)
#
# from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
#
#
# from datetime import date, timedelta
# import os
#
# # Copernicus Open Access Hub 登录信息
# USERNAME = 'xinyu.yan@tus.ie'
# PASSWORD = 'Yxy19890723!'
# from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
# from datetime import date
#
# # 使用你的 Copernicus SciHub 账号登录
#
# # 示例：用 product_id 下载（替换为你从 query 查询到的 ID）
# product_id = 'eb1fe961-0b2d-4e4f-8d21-8c0605255240'
#
# # 登录 API（使用 Copernicus SciHub）
#
import requests
# from datetime import datetime, timedelta
# import os
#
# # === Step 1: 获取 Access Token ===
#
username = 'xinyu.yan@tus.ie'
password = 'Yxy19890723!'
token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
token_payload = {
    'grant_type': 'password',
    'client_id': 'cdse-public',
    'username': username,
    'password': password
}

token_response = requests.post(token_url, data=token_payload)
if token_response.status_code != 200:
    print("❌ 获取 Access Token 失败")
    print(token_response.text)
    exit()

access_token = token_response.json()['access_token']
print("✅ Access Token 获取成功")
#
# # === Step 2: 查询 Athlone 附近的 Sentinel-2 L2A 产品 ===
# headers = {
#     'Authorization': f'Bearer {access_token}'
# }
#
# end_date = datetime.utcnow()
# start_date = end_date - timedelta(days=30)
#
# query_url = (
#     "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
#     f"?$filter=Collection/Name eq 'SENTINEL-2' and contains(Name,'T29UNV') and contains(Name,'MSIL2A') and "
#     f"ContentDate/Start gt {start_date.isoformat()}Z and ContentDate/Start lt {end_date.isoformat()}Z"
#     "&$orderby=ContentDate/Start desc&$top=1"
# )
#
# response = requests.get(query_url, headers=headers)
# if response.status_code != 200:
#     print("❌ 查询失败")
#     print(response.text)
#     exit()
#
# products = response.json().get("value", [])
# if not products:
#     print("⚠️ 没有找到符合条件的产品")
#     exit()
#
# product = products[0]
# product_id = product["Id"]
# product_name = product["Name"]
# print(f"📦 找到产品: {product_name}")
# print(f"🆔 产品ID: {product_id}")
#
# # === Step 3: 下载产品（zip格式） ===
# download_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$zip"
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "User-Agent": "Mozilla/5.0"
# }
#
# response = requests.get(download_url, headers=headers, stream=True)
#
# if response.status_code == 200:
#     with open(f"{product_name}.zip", "wb") as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             if chunk:
#                 f.write(chunk)
#     print(f"✅ 下载成功: {product_name}.zip")
# else:
#     print(f"❌ 下载失败，状态码: {response.status_code}")
#     print(response.text)
# import datetime
# import requests
# # 定义搜索参数
# search_url = "https://catalogue.dataspace.copernicus.eu/stac/search"
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }
#
# # Athlone 地区的经纬度边界框（bbox）：[西经, 南纬, 东经, 北纬]
# bbox = [-8.0, 53.3, -7.9, 53.4]  # 请根据实际需求调整
#
# # 定义时间范围，例如过去30天
# end_date = datetime.datetime.utcnow()
# start_date = end_date - datetime.timedelta(days=30)
# datetime_range = f"{start_date.isoformat()}Z/{end_date.isoformat()}Z"
#
# # 构建搜索请求体
# search_payload = {
#     "collections": ["SENTINEL-2"],
#     "bbox": bbox,
#     "datetime": datetime_range,
#     "limit": 5
# }
#
# # 发送搜索请求
# response = requests.post(search_url, headers=headers, json=search_payload)
#
# if response.status_code == 200:
#     search_results = response.json()
#     items = search_results.get("features", [])
#     if not items:
#         print("⚠️ 没有找到符合条件的产品")
#     else:
#         print(f"✅ 找到 {len(items)} 个产品")
#         for item in items:
#             print("\n📦 产品名称:", item["id"])
#             print("🕒 时间:", item["properties"]["datetime"])
#             assets = item.get("assets", {})
#             if "thumbnail" in assets:
#                 print("🖼️ 快速预览图像链接:", assets["thumbnail"]["href"])
#             if "product" in assets:
#                 print("📥 数据下载链接:", assets["product"]["href"])
# else:
#     print(f"❌ 搜索失败，状态码: {response.status_code}")
#     print(response.text)
# import requests
#
# # 示例产品 ID（你可以更换为其他产品）
# product_asset_href = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products(你的产品ID)/$value"
#
# # Copernicus 账号信息
# USERNAME = 'xinyu.yan@tus.ie'
# PASSWORD = 'Yxy19890723!'
# TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
#
# # 获取 Access Token
# response = requests.post(TOKEN_URL, data={
#     "grant_type": "password",
#     "client_id": "cdse-public",
#     "username": USERNAME,
#     "password": PASSWORD
# })
#
# if response.status_code == 200:
#     access_token = response.json()['access_token']
#     headers = {"Authorization": f"Bearer {access_token}"}
#
#     # 开始下载产品
#     output_file = "sentinel2_download.zip"
#     r = requests.get(product_asset_href, headers=headers, stream=True)
#
#     if r.status_code == 200:
#         with open(output_file, "wb") as f:
#             for chunk in r.iter_content(1024 * 1024):
#                 f.write(chunk)
#         print(f"✅ 下载成功，文件保存为: {output_file}")
#     else:
#         print(f"❌ 下载失败，状态码: {r.status_code}")
#         print(r.text)
# else:
#     print(f"❌ 获取访问令牌失败: {response.status_code}")
#     print(response.text)
import requests
import datetime
import os

# === 用户名和密码 ===
USERNAME = 'xinyu.yan@tus.ie'
PASSWORD = 'Yxy19890723!'

# === 获取 Access Token ===
print("🔐 获取访问令牌中...")
token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
payload = {
    'grant_type': 'password',
    'client_id': 'cdse-public',
    'username': USERNAME,
    'password': PASSWORD
}
token_response = requests.post(token_url, data=payload)

if token_response.status_code == 200:
    token_data = token_response.json()
    access_token = token_data["access_token"]
    print("✅ Access Token 获取成功")
else:
    print(f"❌ 获取 Token 失败: {token_response.status_code}")
    print(token_response.text)
    exit()

# === 查询 Sentinel-2 产品 ===
print("🔍 查询 Sentinel-2 Athlone 产品中...")

search_url = "https://catalogue.dataspace.copernicus.eu/stac/search"
headers = {"Authorization": f"Bearer {access_token}"}

end_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

params = {
    "collections": ["SENTINEL-2"],
    "datetime": f"{start_date}/{end_date}",
    "limit": 5,
    "bbox": [-8.0, 53.3, -7.5, 53.5]  # Athlone 区域
}

response = requests.post(search_url, headers=headers, json=params)
if response.status_code != 200:
    print(f"❌ 查询失败: {response.status_code}")
    print(response.text)
    exit()

data = response.json()
features = data.get("features", [])
if not features:
    print("⚠️ 没有找到符合条件的产品。")
    exit()

# === 显示第一个产品信息 ===
i=0
for feature in features:
    first_item = feature
    product_name = first_item["properties"].get("title", first_item["id"])
    print(f"✅ 找到产品: {product_name}")

    # === 下载 quicklook ===
    assets = first_item.get("assets", {})
    quicklook_url = assets.get("thumbnail", {}).get("href") or assets.get("QUICKLOOK", {}).get("href")

    if quicklook_url:
        print(f"⬇️ 正在下载 Quicklook: {quicklook_url}")
        img_response = requests.get(quicklook_url, stream=True)
        if img_response.status_code == 200:
            with open(f"quicklook{i}.jpg", "wb") as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Quicklook 已保存为 quicklook{i}.jpg")
        else:
            print(f"❌ Quicklook 下载失败: {img_response.status_code}")
    else:
        print("⚠️ 没有 Quicklook 链接可用。")

    i+=1