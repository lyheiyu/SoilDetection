import requests
import json
# 把你的 token 粘贴在这里（保持字符串完整）
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzQ2Njk5MDE3LCJpYXQiOjE3NDY2OTkwMTcsImV4cCI6MTc0NjcwMjYxNywiYXVkIjoiYXBpIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImFwaSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHMiLCJzdWIiOiJiNTJkYTA4YThhOWM0Yzc5YWFlZTFlOGQ3NjU4NzE1MCIsImF1dGhfdGltZSI6MTc0NjE3ODQ3NiwiaWRwIjoibG9jYWwiLCJzaWQiOiJDN0MwMkI0REI2QTQwNThBODM1MzVEMkZCREQ2MEJDNCIsImF6cCI6ImZhcm1tYXBzIiwianRpIjoiNENBNzQ2MEIwNzdFODI0MEU1RkRFOUQ2QzgxNzZEQzQifQ.pRvWIWeJdAv5bolvsgSkq9OP9L8pDnFySwF1VfLBgYMnccBrfwdi3GLzGyenDkH9VkBCWEOGKfityhPG4t-8ScPF8-7qqm_l0YOKO0zOI7E48yTU7HFCW0yyM7eDi02a21QlgnfyuM8UO4O3bmnc0z_lGU8OD_C8VMVI-HmUrbSkJr3iuKjYSxE5JF9sBSqahECTu04kCYidXg3wa8t-Sc4VXWSdAoSpe-o3VM1-bQgVdjPuUZfDVJ1bPbKfhi_GiTGtVbz1JLgnzadA0OwJRX9Vi0aQLuAQQEsFf5A01f_06gPAW_S1LFISNvMTjKFxaqovoTkX15gRha-98VqWkdcKGWRJPbIIXBOnY0j3GtjLPxR5rDPR5u7rzSrWWGdTV1CoBOcuT23YqZxxeqXZhi8JnUT3hFguckaWJHtSNJTIsLrAIOfXVnROdeBgeHqWPN0l4esOQW43ZGj_In2qUjIS4lEL5pl2p0y8o4OlAz7lBhgPwsopV_HYlPGLWHWgWiJtWfcceZ_b_h1qIaHe99_JH0EoUZnVJAXdgU7QXVlT4S3YkfosqgoRKnFIWUh-SY4c6NoEpljnRDD0nm4xrTHmKyi-D4X4arxHJo812qqqHlbLV33tmw-gLqx6-FFGjTTa7EFw0lRxbLYulupC79hvAswXWQDPT5RkLSpLERQ"

username = "soilcratesll@gmail.com"
password = "Soilcrates2025!"

token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMTU0NjIwLCJpYXQiOjE3NTAxNTQ2MjAsImV4cCI6MTc1MDE1ODIyMCwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IkY0MjU3NEQ1RjhGMEI5QTE4NUQxNTcyNjhGODk0RTVGIn0.e0txWsdsCI8_17A-ek4w0IhY2Jgyiq4AItXGhDchVpxPHvJb9pCgfB09QjHmmcZp4cusYd8XFlS1lLNCPRntLL6Hcg0mPddFrJAj8uzhjf47t0vEqmXgWfpEc1-tQqJvnpWHyQ6Xp_G2r_RSHuBsRNpkvjbuR0K-UR5Vb7B_LbmQGVSwPNYdIJ1-zWRW8s6CHKi6md5GWBdk0GupHr9Ml2KSXaEixIIJLC-7X1r6Wbwx4eQKxZpeKT6l-dbg1WCDlOrdiRlJl9j1NiqXo1PRhsY2awWX8hWcIaNy1Q8qVlgnEcGoLVHYYzniWE9mrV6rlSdQuyhplsf4xVha_7QlFE09BAJGrIeiFOOxE1p5ACI93TjIinZpHtELSoegKLVEHlEt5UHvwX39F-6wdbccAsdoK2jx_vheHYxuxYRNrwJksw9q3V4Q6chlEMr6dPJU7_pQ-bvPvXtSE5XFoOl3OVFiArGomEa4bIW1iBBkmoG1mJcvIlgDvcWor7nuT6_lPC48rFTQksLI3PJf-iyZWZP_psm2NeOfOuRNWHKoLxrdUDYVONOV6_0vMiqXPXsgLx9rC9SHdcq-OkDmJ1J3_09W1s8TVcPuqLGBY8tr3THPbWjA5G1qXKYJXLJnmnOZPfqhfEBpmCAxdDJZZG75Kg-1dDHyo0SX8oxIWA5wE-Y'
headers = {
    "Authorization": f"Bearer {token}",
    'username': username,
    'password': password,
    'Content-Type': 'application/json'
}

response = requests.get("https://farmmaps.eu/api/v1/folders/my_drive/", headers=headers)
cropfield_code = "1a58ec4e5bc84891931188cf90dfe3ea"

r = requests.get(f"https://farmmaps.eu/api/v1/items/{cropfield_code}", headers=headers)
print(json.dumps(r.json(), indent=2))

if response.ok:
    data = response.json()
    print("✅ parentCode:", data["code"])
else:
    print("❌ 获取失败:", response.status_code)
secondfield=[
            [6.10331686552072,53.0701314102389],
            [6.10380013552072,53.0704604102389],
            [6.10430013552072,53.0709904102389],
            [6.10453013552072,53.0712404102389],
            [6.10485013552072,53.0715604102389],
            [6.10490013552072,53.0716004102389],
            [6.10530013552072,53.0713504102389],
            [6.10565013552072,53.0711004102389],
            [6.10610013552072,53.0708004102389],
            [6.10645013552072,53.0705604102389],
            [6.10660013552072,53.0704304102389],
            [6.10659013552072,53.0704104102389],
            [6.10630013552072,53.0702404102389],
            [6.10510013552072,53.0696004102389],
            [6.10490013552072,53.0694904102389],
            [6.10420013552072,53.0697404102389],
            [6.10331686552072,53.0701314102389]
        ]

cropfield = {
    "parentCode":  data["code"],
    "itemType": "vnd.farmmaps.itemtype.cropfield",
    "name": "MyCropfield 2025-MultiPolygon",
    "dataDate": "2025-03-01T00:00:00Z",
    "dataEndDate": "2025-10-01T00:00:00Z",
    "data": {
    # "area": 2.02,
    "final": True,
    "soilCode": "7",
    "soilName": "Clay",
    "varietyCode": "10923",
    "varietyName": "Barturbo",
    "cropTypeCode": "1050106",
    "cropTypeName": "Annual ryegrass",
    "rootDepthMax": 4,
    # "emergenceDate": None,
    "productionPurposeCode": "118",
    "productionPurposeName": "cover crop"
  },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [6.09942873984307,53.070025028087],
            [6.09992507404607,53.0705617890585],
            [6.10036959220086,53.0710679529031],
            [6.10065149010421,53.0714062774307],
            [6.10087493644271,53.0716712354474],
            [6.10091082982487,53.0716936039203],
            [6.10165087441291,53.0712041549161],
            [6.10204994718318,53.0709349338005],
            [6.10263143118855,53.0705789370018],
            [6.10311578125011,53.0702657538294],
            [6.10331686552072,53.0701314102389],
            [6.103326530575,53.070119463569],
            [6.10309137950343,53.0699829669055],
            [6.10184241586523,53.0692902201371],
            [6.10168497998891,53.0691984306747],
            [6.10092987659869,53.0694894453514],
            [6.09942873984307,53.070025028087]
        ],
        ]
    }
}
#

response = requests.post("https://farmmaps.eu/api/v1/items", headers=headers, data=json.dumps(cropfield))

if response.status_code in [200, 201]:
    print("create field successfully:", response.json()["code"])
    code=response.json()["code"]
else:
    print("❌ create field failed:", response.status_code, response.text)
import requests

API_BASE_URL = "https://farmmaps.eu"

ITEMCODE = code  # 你的地块 ID

headers = {
    "Authorization": f"Bearer {token}"
}
response = requests.post(
    f"{API_BASE_URL}/api/v1/items/{ITEMCODE}/tasks",
    headers=headers,
    json={"taskType": "vnd.farmmaps.task.workflow"}
)

if response.status_code == 201:
    task_code = response.json()["code"]
    print("✅ Workflow 任务已创建，任务代码：", task_code)
else:
    print("❌ 创建失败:", response.status_code, response.text)
import time

# tasklist
while True:
    r = requests.get(
        f"{API_BASE_URL}/api/v1/items/{ITEMCODE}/tasks",
        headers=headers
    )
    print(r.json())
    tasks = r.json()
    for task in tasks:
        print(f"type: {task['taskType']}，status: {task['state']}，taskId: {task['code']}")
    time.sleep(5)