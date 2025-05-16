import json
import os


# 读取配置文件中的 API 密钥
def load_api_key():
    """
    从本地配置文件中加载 API 密钥
    """
    config_path = os.path.join(os.getcwd(), "config.json")
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            api_key = config.get("api_key")
            if not api_key:
                raise ValueError("API key not found in config.json.")
            return api_key
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file 'config.json' not found in {os.getcwd()}.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding config.json. Ensure it is properly formatted.")


# 示例 API 调用函数
def fetch_data_from_api(endpoint):
    """
    使用 API 密钥调用指定的 API 端点
    """
    import requests

    api_key = load_api_key()
    base_url = "https://example-api.com"  # 替换为你的实际 API 基础 URL
    url = f"{base_url}/{endpoint}"

    params = {
        "appid": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


# 示例用法
if __name__ == "__main__":
    endpoint = "data_endpoint"  # 替换为实际的 API 端点
    result = fetch_data_from_api(endpoint)
    if result:
        print("API Response:", result)
