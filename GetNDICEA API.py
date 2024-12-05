import requests

# API URL
url = "https://ndiceaweb.eu/api/RequestToken"

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 请求体
data = {
    "UserName": "your_username",  # 替换为您的用户名
    "Password": "your_password"  # 替换为您的密码
}

try:
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 打印返回的令牌
        token = response.json().get("token")
        print("Token:", token)
    else:
        print(f"Error: {response.status_code}")
        print("Response Content:", response.text)

except Exception as e:
    print("An error occurred:", e)
