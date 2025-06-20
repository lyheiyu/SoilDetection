import os
import requests
import time
token = ' eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMzQ5NzY5LCJpYXQiOjE3NTAzNDk3NjksImV4cCI6MTc1MDM1MzM2OSwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IkM5RDEwRkQ2NEI3MDBCQTEwNDE0RTZENUNDODNERTNBIn0.ptnQXqdgC49cJ6UFCGdrmVALQlPSfcmVeXVcrPTaVeAgR2PpesoxLniRAwSzNTxjN2qDH4rzqIxjim1YKe3-xJSf_rXOGiT3OXpl2IwuFd91DlEzxx0xvNvuxf6uWhKjzw0P5krgDSZOIKaKb7B4y64jffTS00AUXFtkt0m1VKeMS8wOO67fScFo8MtSqNqRdYb6_C5Wfxrr7yUeE7c9M9hdGJ7eAUN_zdURuyzubPzp7hOsIYYxGnCeB0U1EotMMBXd5_-BKmWU9ZGJQj5dtLAsuGTHyoxst31DZbw01TzIkxl2IscV2Qy94hXUQKIgo4rFBDyDv_58SOqH-ZaGBCVHHy3eIu2ROKhNy_VYnZhy2aTQDwOroJYT9LxiHcURm4oRTrdnEYPP6iJ7SjrH7pY_z3SRxJNM3VkmUf0pLU4H_Y4MbeUD6OD0dzIagtX5wXd7tRcvBBamjA3BSsfTBoElFfhFN1ZDcIc2mkdSi90GKq96mnWGuwNSdul2QDx8oF0uaCnTV_S-wPtr7VjfMnx_Ydo2FQRHHLyuCWSOC0x9BCvMoSr_d3HH2Z9DnrkJZt4U9xxMwCl51ApKJJsl2cc3oz1J7HKRbSgd3z7LJPpb5WQn6qtLNPv0IEEUPRYFsrWj5DoXpiw7lBzjSKk8ccHfkWTsTIsUQXU4QdRZMxQ'
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
time.sleep(2)
# # upload_url = f"https://farmmaps.eu/api/v1/items/{file_code}/mapimage"
# mapimage
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/mapimage'
# mapimage
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/mapimage/0'
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/tiles/0/1/1/1.png'
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/tiles/1/1/1.png'
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/vectortiles/1/1/1.pdf'
# upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/vectortiles/1/1/2.pbf'
upload_url=f'https://farmmaps.eu/api/v1/items/{file_code}/vectortiles/image_tiles/0/1/2/1.png'
headers = {
    "Authorization": f"Bearer {token}",
    "accept": "*/*"
}

# 模拟 multipart/form-data 文件上传
# files = {
#     'chunk': (file_path, open(file_path, 'rb'), 'image/tiff')
# }

response = requests.get(upload_url, headers=headers)

print("✅ Status Code:", response.status_code)
print("📄 Response:", response.text)

# response.raise_for_status()