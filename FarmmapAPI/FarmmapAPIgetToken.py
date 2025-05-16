import requests

# ✅ 你自己的 FarmMaps 登录信息（用你真实的账号密码）
username = "soilcratesll@gmail.com"
password = "Soilcrates2025!"

# ✅ 试用默认 client_id
client_id = "farmmapstesteu_swagger"  # 这个是公开 web 客户端
token_url = "https://accounts.farmmaps.eu/connect/token"
import requests

url = 'https://accounts.farmmaps.eu/connect/token'

data = {
    'grant_type': 'password',
    'client_id': 'farmmaps_swagger',  # 注意：这里必须是一个允许 password 授权的 client
    'username': username,
    'password': password,
    'scope': 'api openid profile'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, data=data, headers=headers)

if response.status_code == 200:
    token = response.json().get('access_token')
    print('✅ Access Token:', token)
else:
    print('❌ Failed to get token:', response.status_code, response.text)
