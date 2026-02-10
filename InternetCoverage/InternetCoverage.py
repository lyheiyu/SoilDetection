import requests
import pandas as pd
import time

BASE_URL = "https://services6.arcgis.com/clPWQMwZfdWn4MQZ/ArcGIS/rest/services/Internet_Connectivity/FeatureServer/100/query"

all_rows = []
offset = 0
batch = 2000  # ArcGIS limit

while True:
    params = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "True",
        "resultRecordCount": batch,
        "resultOffset": offset
    }

    r = requests.get(BASE_URL, params=params)
    data = r.json()

    # 如果没有 features，就结束
    if "features" not in data or len(data["features"]) == 0:
        break

    rows = [f["attributes"] for f in data["features"]]
    all_rows.extend(rows)

    print(f"Downloaded {len(rows)} records (offset={offset})")

    offset += batch
    time.sleep(0.2)  # 小延时避免服务器压力太大

df = pd.DataFrame(all_rows)

# 保存成 CSV
df.to_csv("internet_connectivity_full.csv", index=False)

print("下载完成，总记录数：", len(df))
