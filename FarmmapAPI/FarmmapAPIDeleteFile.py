import os
import requests
import time
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMTc2MzAyLCJpYXQiOjE3NTAxNzYzMDIsImV4cCI6MTc1MDE3OTkwMiwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IjBEODBEMEVFMjlDOEZBRkIyQjUwREIyMjk3NDVBNzVFIn0.pV4I07Q18WkV5PqWEI-3FE2r2wE6aJfyHupcm-UH7maM0e-_92OdhcI7MJ_QUtPFohOBQkJxiqanl5xP7pP8ilGxvSrZ8pamsDbdCRW2Bh1mBmUSvtYjB-X3AmdNfcqF36cx73yhzkcpWshvHixfWHQMj6XvycRkSC6KZXFROZa6UKGyET53XK6OIfBI5ZwfFnJ7NZ9YAQB4O-xz3ZfgdTjMAtq5UCSCMkx1WStWQDPCSaY5xIhZpvO8V_Lv1NSfaXHZ4GIpLYMiWIEp0KAJjzZRd9JgZxoSF5GCxd0A8ryXqUgEl-OBYtP-VzrC2do6v4EdPUrAUVQYWqxqb3mbP3hGygUiHDOBlmjeBRBIRbd5gK4P_B0ZquNxYu5XONyJX0Wbc1ntqk4ZwOAVuW0e1dBij2N9UZYM1-hzX3vmN3h7WCpKH2qKVaR5uS9wV218ioypd23LOi3ZDRp3QlpYU-elNJPmPFkHcJCv2DIuy29cO3lNhNwCqQ9yM4oejNc-2acF1ALv_0cpCPpxrIJDRqW45G86troFlVqHNIir8bHROITKZZdkAsFrbyIR9E_iNqiXrz5clQfbT72QgFwriijOiau1ePX2uu3b_r71som6oD7jQ3XstY872cHd-nkewI2ywj_HTo28LUBSwvodj5Kb9ooED18P2X-sUrg9sUA'
# file_path = "C:\D\projects\SoilDetection\SoilDetection\ireland_soil_pH.tif"
# file_path = "C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\\tifFile\\spain_soil_ph.tif"
file_path = r"C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\tifFile\spain_soil_ph.tif"
parent_code = "25ef92b2fa2745ef8271de9930b47fd6"

# Step 1: 注册文件
file_size = os.path.getsize(file_path)
file_name = os.path.basename(file_path)


file_code='33ac8d0067e34275b974bfc72dae3d95'

url = f"https://farmmaps.eu/api/v1/file/{file_code}"
headers = {
    "Authorization": f"Bearer {token}",
    "accept": "*/*"
}

# 发送 DELETE 请求
response = requests.delete(url, headers=headers)

# 输出结果
print("✅ 状态码:", response.status_code)
print("📄 返回信息:", response.text)

response = requests.get(f"https://farmmaps.eu/api/v1/file/{file_code}", headers={
    "Authorization": f"Bearer {token}"
})
print(response.status_code)  # 200 说明还在；404 说明真的被删除