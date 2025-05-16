import requests

# url = "https://ndiceaweb.eu/api/Scenario/GetAvailableSoils"
#
# headers = {
#     "Content-Type": "application/xml"
# }
#
# # XML 请求体（注意 xmlns 必须一模一样）
# xml_data = """
# <ArrayOfItem xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.datacontract.org/2004/07/Ndicea.Mvc.Models.Api">
#   <Item>
#     <Id>1</Id>
#     <NameDe>sample string 4</NameDe>
#     <NameEn>sample string 3</NameEn>
#     <NameNl>sample string 2</NameNl>
#   </Item>
#   <Item>
#     <Id>1</Id>
#     <NameDe>sample string 4</NameDe>
#     <NameEn>sample string 3</NameEn>
#     <NameNl>sample string 2</NameNl>
#   </Item>
# </ArrayOfItem>
# """
#
# response = requests.get(url, data=xml_data.strip(), headers=headers)
#
# print("Status Code:", response.status_code)
# print("Response:", response.text)

# data = {
#     "UserName": "xinyu.yan@tus.ie",
#     "Password": "dsCbjTKM7uLEWANPzwe69t"
# }

url = "https://ndiceaweb.eu/api/RequestToken"
headers = {"Content-Type": "application/json"}
data = {
    "UserName": "xinyu.yan@tus.ie",
    "Password": "dsCbjTKM7uLEWANPzwe69t"
}

# ✅ Step 1: Prepare
url = "https://ndiceaweb.eu/api/RequestToken"
headers = {
    "Content-Type": "application/json"
}
data = {
    "UserName": "xinyu.yan@tus.ie",
    "Password": "dsCbjTKM7uLEWANPzwe69t"
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
except:
    print("Response is not valid JSON")


xml_data = """
<AuthModel xmlns:i="http://www.w3.org/2001/XMLSchema-instance"
           xmlns="http://schemas.datacontract.org/2004/07/Ndicea.ApiHelper.Models">
  <Password>dsCbjTKM7uLEWANPzwe69t</Password>
  <UserName>xinyu.yan@tus.ie</UserName>
</AuthModel>
"""

headers = {
    "Content-Type": "application/xml"
}

response = requests.post(url, data=xml_data.encode("utf-8"), headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)


headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "UserName": "xinyu.yan@tus.ie",
    "Password": "dsCbjTKM7uLEWANPzwe69t"
}

response = requests.post(url, data=data, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)