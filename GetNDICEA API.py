# import requests
#
# # API URL
# url = "https://ndiceaweb.eu/api/RequestToken"
#
# # 请求头
# headers = {
#     "Content-Type": "application/json"
# }
#
# # 请求体
# data = {
#     "UserName": "xinyu.yan@tus.ie",  # 替换为您的用户名
#     "Password": "kdjjK&4!O5oTuor6"  # 替换为您的密码
# }
#
# try:
#     # 发送 POST 请求
#     response = requests.post(url, headers=headers, json=data)
#
#     # 检查响应状态码
#     if response.status_code == 200:
#         # 打印返回的令牌
#         token = response.json().get("token")
#         print("Token:", token)
#     else:
#         print(f"Error: {response.status_code}")
#         print("Response Content:", response.text)
#
# except Exception as e:
#     print("An error occurred:", e)
import json

import requests

# ✅ Step 1: Prepare
url = "https://ndiceaweb.eu/api/RequestToken"
headers = {
    "Content-Type": "application/json"
}
data = {
    "UserName": "xinyu.yan@tus.ie",  # replace with your actual username
    "Password": "kdjjK&4!O5oTuor6"             # replace with your actual password
}

# ✅ Step 2: Send POST to get token
response = requests.post(url, json=data, headers=headers)

# ✅ Step 3: Handle response
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Optional: try parsing JSON token
try:
    token_data = response.json()

    print("Parsed Token:", token_data)
    # get the accessToken in token_data
    access_token = token_data["AccessToken"]
    print("Access Token:", access_token)
    json.dump(token_data, open("token.json", "w"))
except:
    print("Response is not valid JSON")


import requests

# Your token here

import requests

# 替换为你的真实 Token


# NDICEA API endpoint
# import requests
#
# # Replace with your actual Bearer token
#
# # 请求头
# # Headers
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Accept": "application/json"
# }
#
# # ✅ 正确的 GET URL
# url = "https://ndiceaweb.eu/api/Scenario/GetAvailableRegions"
#
# # ✅ 发送 GET 请求（❗不要用 POST）
# response = requests.get(url, headers=headers)
#
# print("Status Code:", response.status_code)
# print("Response Text:", response.text)
#
# if response.status_code == 200:
#     regions = response.json()
#     for region in regions:
#         print(f"ID: {region['Id']} | EN: {region['NameEn']}")
# else:
#     print("❌ Failed with status:", response.status_code)


headers = {
    "Authorization": f"Bearer {access_token.strip()}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

url = "https://ndiceaweb.eu/api/v6/RunModel"

# payload = {
#     "Id": 1,
#     "ScenName": "Valid NDICEA Scenario",
#     "RegioId": 2,
#     "startDate": "2024-01-01",
#     "endDate": "2024-12-31",
#     "Soil": {
#         "EvaporationFactorBare": 0.25,
#         "SomStart": 2.0,
#         "Ph": 6.5,
#         "MinWaterUptake": 0.75,
#         "CNSoilLife": 6.5,
#         "ADSoilLife": 0.4,
#         "NFixThreshold": 15.0,
#         "Tillage": 0,
#         "NContentGroundwater": 15.0,
#         "CapillaryRiseMax": 3.0,
#         "Depth": 30.0,
#         "SoilRootdepthMax": 70.0,
#         "GwLevelDeepSummerDay": 196,
#         "GwLevelHighWinterDay": 46,
#         "GwLevelDeepSummer": 120.0,
#         "GwLevelHighWinter": 80.0,
#         "TopLayer": {
#             "SoilSourceId": 6,
#             "NLeachingFactor": 0.85,
#             "DenitrificationFactor": 0.1,
#             "DecayFactor": 0.86,
#             "NmineralStart": 20.0,
#             "SoilWaterSaturated": 0.5,
#             "MoistureCurveFactor": 0.011,
#             "CapillaryRiseDistance": 114.9,
#             "CapillaryRiseReduction": 44.0,
#             "InitialWaterPressure": 100.0,
#             "WaterBypassFlowBench": 0.0,
#             "WaterBypassFlowFactor": 0.0,
#             "TextConventTillage": 0.0,
#             "TextReducedTillage": 0.0,
#             "TextNoTillage": 0.0,
#             "CecScaler": 0.0,
#             "BulkDensity": 1.35,
#             "SOMOldQuant": 71600.0,
#             "SOMYoungQuant": 6600.0,
#             "SOMFreshQuant": 2800.0,
#             "NContentOmYoung": 4.5,
#             "NContentOmOld": 5.8,
#             "NContentOmFresh": 3.0,
#             "VirtualInitialAgeYoung": 4.0,
#             "VirtualInitialAgeOld": 24.0,
#             "VirtualInitialAgeFresh": 1.4
#         },
#         "SecondLayer": {
#             "SoilSourceId": 6,
#             "NLeachingFactor": 0.85,
#             "DenitrificationFactor": 0.1,
#             "DenitrificationThreshold": 5.0,
#             "DecayFactor": 0.86,
#             "NmineralStart": 20.0,
#             "SoilWaterSaturated": 0.5,
#             "MoistureCurveFactor": 0.011,
#             "CapillaryRiseDistance": 114.9,
#             "CapillaryRiseReduction": 44.0,
#             "InitialWaterPressure": 100.0,
#             "WaterBypassFlowBench": 0.0,
#             "WaterBypassFlowFactor": 0.0,
#             "TextConventTillage": 0.0,
#             "TextReducedTillage": 0.0,
#             "TextNoTillage": 0.0,
#             "CecScaler": 0.0
#         }
#     },
#     "Crops":
#         {
#             "CropId": 0,
#             "ScenarioId": 0,
#             "CultureName": "Potato organic",
#             "DateSowing": "2022-04-19T00:00:00",
#             "DateFullGrowth": "2022-06-18T00:00:00",
#             "DateStartRipening": "2022-07-26T00:00:00",
#             "DateHarvest": "2022-07-26T00:00:00",
#             "Yield": 35000.0,
#             "ProductIncorporated": 1.0,
#             "ResidueIncorporated": 1.0,
#             "RootIncorporated": 1.0,
#             "DmContentProduct": 21.0,
#             "NfixMax": 0.0,
#             "TranspirationFactor": 1.1,
#             "RootDepthGrowth": 0.07,
#             "CropRootDepthMax": 80.0,
#             "SeedQuant": 2000.0,
#             "DmContentSeed": 23.0,
#             "NContentDMSeed": 1.57,
#             "P2O5ContentSeed": 0.59,
#             "K2OContentSeed": 2.72,
#             "TempMinimum": 0.0,
#             "TempSumMinimum": 30.0,
#             "GreenHarvest": False,
#             "DmRatioProduct": 0.7,
#             "DmRatioResidue": 0.25,
#             "DmRatioRoot": 0.05,
#             "NcontentDmProduct": 1.5,
#             "NcontentDmResidue": 2.2,
#             "NcontentDmRoot": 1.0,
#             "P2O5ContentDmProduct": 0.59,
#             "P2O5ContentDmResidue": 0.83,
#             "P2O5ContentDmRoot": 0.0,
#             "K2OContentProduct": 2.72,
#             "K2OContentResidue": 3.3,
#             "K2OContentRoot": 0.0,
#             "InitialAgeProduct": 0.99,
#             "InitialAgeResidue": 0.99,
#             "InitialAgeRoot": 1.57,
#             "RootStartDepth": 5.0,
#             "GrassClover": 0,
#             "GrasLandPeriodeType": 0,
#             "RootDistribution": 0.03,
#             "Tbase": 7.0,
#             "DmPercResi": 10.0
#         },
#     "GreenManures": [],
#     "Grasses": [],
#     "Fertilizers":  {
#             "FertilizerId": 0,
#             "ScenarioId": 0,
#             "Name": "Rundvee drijfmest",
#             "Date": "2022-05-01T00:00:00",
#             "Quantity": 10000.0,
#             "NContent": 4.1,
#             "P2O5Content": 1.5,
#             "K2OContent": 5.8,
#             "DM": 90.0,
#             "OM": 66.0,
#             "NMineralContent": 2.6,
#             "InitialAge": 1.95,
#             "AmmoniumEmission": 3,
#             "Soort": 0
#         },
#     "Irrigations": []
# }
payload = {
    # "Id": 1,
    "ScenName": "Demo with 1 crop and 1 fertilizer",
    "RegioId": 2,
    "Soil": {
        "EvaporationFactorBare": 0.25,
        "SomStart": 2.0,
        "Ph": 7.0,
        "MinWaterUptake": 0.75,
        "CNSoilLife": 6.5,
        "ADSoilLife": 0.4,
        "NFixThreshold": 15.0,
        "Tillage": 0,
        "NContentGroundwater": 15.0,
        "CapillaryRiseMax": 3.0,
        "Depth": 30.0,
        "SoilRootdepthMax": 70.0,
        "GwLevelDeepSummerDay": 196,
        "GwLevelHighWinterDay": 46,
        "GwLevelDeepSummer": 120.0,
        "GwLevelHighWinter": 80.0,
        "TopLayer": {
            "SoilSourceId": 6,
            "NLeachingFactor": 0.85,
            "DenitrificationFactor": 0.1,
            "DecayFactor": 0.86,
            "NmineralStart": 20.0,
            "SoilWaterSaturated": 0.47,
            "MoistureCurveFactor": 0.011,
            "CapillaryRiseDistance": 114.9,
            "CapillaryRiseReduction": 44.0,
            "InitialWaterPressure": 100.0,
            "WaterBypassFlowBench": 0.0,
            "WaterBypassFlowFactor": 0.0,
            "TextConventTillage": 0.0,
            "TextReducedTillage": 0.0,
            "TextNoTillage": 0.0,
            "CecScaler": 0.0,
            "BulkDensity": 1.35,
            "SOMOldQuant": 71600.0,
            "SOMYoungQuant": 6600.0,
            "SOMFreshQuant": 2800.0,
            "NContentOmYoung": 4.5,
            "NContentOmOld": 5.8,
            "NContentOmFresh": 3.0,
            "VirtualInitialAgeYoung": 4.0,
            "VirtualInitialAgeOld": 24.0,
            "VirtualInitialAgeFresh": 1.4
        },
        "SecondLayer": {
            "SoilSourceId": 6,
            "NLeachingFactor": 0.85,
            "DenitrificationFactor": 0.1,
            "DenitrificationThreshold": 5.0,
            "DecayFactor": 0.86,
            "NmineralStart": 20.0,
            "SoilWaterSaturated": 0.47,
            "MoistureCurveFactor": 0.011,
            "CapillaryRiseDistance": 114.9,
            "CapillaryRiseReduction": 44.0,
            "InitialWaterPressure": 100.0,
            "WaterBypassFlowBench": 0.0,
            "WaterBypassFlowFactor": 0.0,
            "TextConventTillage": 0.0,
            "TextReducedTillage": 0.0,
            "TextNoTillage": 0.0,
            "CecScaler": 0.0
        }
    },
    "Crops": [
        {
            "CropId": 0,
            "ScenarioId": 0,
            "CultureName": "Potato organic",
            "DateSowing": "2022-04-19T00:00:00",
            "DateFullGrowth": "2022-06-18T00:00:00",
            "DateStartRipening": "2022-07-26T00:00:00",
            "DateHarvest": "2022-07-26T00:00:00",
            "Yield": 35000.0,
            "ProductIncorporated": 1.0,
            "ResidueIncorporated": 1.0,
            "RootIncorporated": 1.0,
            "DmContentProduct": 21.0,
            "NfixMax": 0.0,
            "TranspirationFactor": 1.1,
            "RootDepthGrowth": 0.07,
            "CropRootDepthMax": 80.0,
            "SeedQuant": 2000.0,
            "DmContentSeed": 23.0,
            "NContentDMSeed": 1.57,
            "P2O5ContentSeed": 0.59,
            "K2OContentSeed": 2.72,
            "TempMinimum": 0.0,
            "TempSumMinimum": 30.0,
            "GreenHarvest": False,
            "DmRatioProduct": 0.7,
            "DmRatioResidue": 0.25,
            "DmRatioRoot": 0.05,
            "NcontentDmProduct": 1.5,
            "NcontentDmResidue": 2.2,
            "NcontentDmRoot": 1.0,
            "P2O5ContentDmProduct": 0.59,
            "P2O5ContentDmResidue": 0.83,
            "P2O5ContentDmRoot": 0.0,
            "K2OContentProduct": 2.72,
            "K2OContentResidue": 3.3,
            "K2OContentRoot": 0.0,
            "InitialAgeProduct": 0.99,
            "InitialAgeResidue": 0.99,
            "InitialAgeRoot": 1.57,
            "RootStartDepth": 5.0,
            "GrassClover": 0,
            "GrasLandPeriodeType": 0,
            "RootDistribution": 0.03,
            "Tbase": 7.0,
            "DmPercResi": 10.0
        }
    ],
    "GreenManures": [],
    "Grasses": [],
    "Fertilizers": [
        {
            "FertilizerId": 0,
            "ScenarioId": 0,
            "Name": "Rundvee drijfmest",
            "Date": "2022-05-01T00:00:00",
            "Quantity": 10000.0,
            "NContent": 4.1,
            "P2O5Content": 1.5,
            "K2OContent": 5.8,
            "DM": 90.0,
            "OM": 66.0,
            "NMineralContent": 2.6,
            "InitialAge": 1.95,
            "AmmoniumEmission": 3,
            "Soort": 0
        }
    ],
    "Irrigations": []
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io
import json

# Assuming the user posted a raw JSON response, we parse it
# response_text = '''{"ScenId":1,"ScenName":"Valid NDICEA Scenario","Message":"Success","Results":[{"Date":"2025-01-01T01:00:00+01:00","Rain":14.8,"Irrigation":0.0,"NminTop":20.0,"NminSecond":20.0,"CumNleaching":0.0,"OrgMatterTop":2.0,"PfTop":2.0},{"Date":"2025-01-02T01:00:00+01:00","Rain":0.7,"Irrigation":0.0,"NminTop":18.7,"NminSecond":21.6,"CumNleaching":-0.1,"OrgMatterTop":2.0,"PfTop":1.87}]}'''  # Shortened for demonstration

# Load the JSON
data = json.loads(response.text)

# Convert results to a DataFrame
df = pd.DataFrame(data["Results"])

# Convert the Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Plot example variables
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["NminTop"], label="NminTop")
plt.plot(df["Date"], df["NminSecond"], label="NminSecond")
plt.plot(df["Date"], df["CumNleaching"], label="CumNleaching")
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("NDICEA Scenario Data Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()


import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the full JSON content (manually truncated here for demo purposes)
# The user already provided a very long JSON string; in practice, this would be parsed from response.

# For demonstration, here's how you would parse the JSON response text:
# json_data = json.loads(response_text)

# Since response_text is not directly passed, here's an example structure:
# example_data = {
#     "Results": [
#         {"Date": "2025-01-01T01:00:00+01:00", "Rain": 14.8, "NminTop": 20.0, "CumNleaching": 0.0},
#         {"Date": "2025-01-02T01:00:00+01:00", "Rain": 0.7, "NminTop": 18.7, "CumNleaching": -0.1},
#         {"Date": "2025-01-03T01:00:00+01:00", "Rain": 3.2, "NminTop": 18.8, "CumNleaching": 0.0},
#         # Add more entries here...
#     ]
# }

# Create DataFrame
df = pd.DataFrame(data["Results"])

# Convert 'Date' column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(df["Date"], df["Rain"], label="Rain (mm)", marker='o')
ax1.set_xlabel("Date")
ax1.set_ylabel("Rain (mm)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Add secondary axis for NminTop and CumNleaching
ax2 = ax1.twinx()
ax2.plot(df["Date"], df["NminTop"], label="NminTop (mg/kg)", color='green', marker='s')
ax2.plot(df["Date"], df["CumNleaching"], label="Cumulative N Leaching (kg/ha)", color='red', marker='^')
ax2.set_ylabel("NminTop / Cumulative N Leaching", color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Date formatting
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()

# Legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title("Rain, NminTop, and Cumulative N Leaching over Time")
plt.tight_layout()
plt.show()

