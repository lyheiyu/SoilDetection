import os
import requests
import json
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import torch
from bs4 import BeautifulSoup

# 加载环境变量
load_dotenv()

# 配置 OpenAI API 风格的本地模型服务端点
BASE_URL = os.getenv('LLAMA3_BASE_URL', 'http://localhost:11434/v1')
API_KEY = os.getenv('LLAMA3_API_KEY', 'llama3:8b')

# 定义头部和端点
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 查询模型信息（可选）
def get_model_info():
    url = f"{BASE_URL}/models"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("Available models:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to fetch models: {response.status_code}")
        print(response.text)

# 生成文本
def generate_text(prompt, model="llama3:8b", max_tokens=200):
    url = f"{BASE_URL}/completions"
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 测试生成
if __name__ == "__main__":
    print("Checking available models...")
    get_model_info()

    print("\nGenerating text...")
    prompt = "Tell me a brief summary of climate change."
    response = generate_text(prompt)
    if response:
        print("Generated text:")
        print(response["choices"][0]["text"])
