import os
import requests
import time
token='eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMjM3OTgzLCJpYXQiOjE3NTAyMzc5ODMsImV4cCI6MTc1MDI0MTU4MywiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzUwMDc3ODc2LCJpZHAiOiJsb2NhbCIsInNpZCI6IjA0REJDQUZCMUJDQkRDRjAxNDZGQTQ3ODM1NjNFRERBIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IjNBQTY5MTE5OERBMUU4NzFDNzg2RkFCNDE5MzFDNTkyIn0.MYGGgDjnHYQVq59wWGTPfskp08Kq7x7KfirVjgckc3uYw_og2yGzFf_A0F99XHNovDg2zeu_kg5xVmzbD6I9MbY4bRmRdESCXl3pvYlhBrmG9_KPG8pUDhQobS-8LnSJg50_0I0dbe2pT5DSbQG9jnS2GxlD0lkQ2XK3LPexKpbKuZnmc63v-ycoDwsZSnMbkd3yHImgxzHX3ntxjLQ6o0K7OBSnNHLiz73D7U4ZuCw7RM7OvHVZr-GHbcMC6ap4tNGuixbpFCZfQ2yhXB37WXdwrFkI9UHkcy_f8AefSiSJiuyTJtp-IkfuWrUXzTvFIuALAyF8vvd2JUjYPIxbgFSxWiM-XGxju6vP_h7KUvNmQR0pZhNCTk2OY9KK8P6AQD2OXLimfmHHMySiSolV02Cp0yeRNDIu7s8TDW5MPnPMj2UUfoJi_WyVsYw13Kl4xKz2zZFp7jRQDgnEdUiSfTuFK7cRTLto5WJZnSGJrnsoA1oJsIZjqYa8u-b3v5hSuT7EBLxm7xEH72m46vRbTb-6Udtcu167aevhlZpPpBs-5oKFGjeu3EOCV5t70kTSayxGSZrUZuIB6FvgRQ3HPFlXyUoxLUD_I3EeBK8aiGYS-r0T20tFPTkEHbkZ0apeWn8GXjypM-cav8wFjKYWG1kFv16E66DK6entZ_ouU-c'
# file_path = "C:\D\projects\SoilDetection\SoilDetection\ireland_soil_pH.tif"
# file_path = "C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\\tifFile\\spain_soil_ph.tif"
file_path = r"C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\tifFile\spain_soil_ph.tif"
parent_code = "25ef92b2fa2745ef8271de9930b47fd6"

# Step 1: 注册文件
file_size = os.path.getsize(file_path)
file_name = os.path.basename(file_path)

reg_response = requests.post(
    "https://farmmaps.eu/api/v1/file",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    },
    json={
        "parentCode": parent_code,
        "name": file_name,
        "size": file_size
    }
)
reg_response.raise_for_status()
reg = reg_response.json()
file_code = reg["code"]
chunk_size = reg["chunkSize"]
print(reg)
print(f"register successfully，file_code: {file_code}, chunkSize: {chunk_size}")

# Step 2: Upload chunk
# file_path = "ireland_soil_pH.tif"
# file_code = "e6e9ec2e841740beaf1cbc97f8a4314e"  # 你从注册接口获取的
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6..."  # 你的有效 Bearer token

upload_url = f"https://farmmaps.eu/api/v1/file/{file_code}/chunk/1"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "*/*"
}

# 模拟 multipart/form-data 文件上传
files = {
    'chunk': (file_path, open(file_path, 'rb'), 'image/tiff')
}

response = requests.post(upload_url, headers=headers, files=files)

print("✅ Status Code:", response.status_code)
print("📄 Response:", response.text)
response.raise_for_status()


url = f"https://farmmaps.eu/api/v1/items/{file_code}/tasks"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "accept": "*/*"
}
payload = {
    "taskType": "vnd.farmmaps.task.geotiff",
    "attributes": {
        "p1": "test",
        "p2": "test2"
    }
}

# 发送 DELETE 请求
response = requests.post(url, json=payload, headers=headers)

# 输出结果
print("status:", response.status_code)
print("return information:", response.text)
#
# response = requests.get(f"https://farmmaps.eu/api/v1/file/{file_code}", headers={
#     "Authorization": f"Bearer {token}"
# })
print(response.status_code)  # 200 说明还在；404 说明真的被删除