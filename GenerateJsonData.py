import pandas as pd
import json
import random

# 预定义可能的土壤查询变量
soil_variables = ["pH", "organic_carbon", "sand", "clay", "silt", "moisture", "nitrogen", "phosphorus"]

# 预定义可能的地理位置
locations = [
    "Dublin, Ireland", "California, USA", "Beijing, China", "New Delhi, India",
    "Berlin, Germany", "Tokyo, Japan", "London, UK", "Sydney, Australia",
    "Paris, France", "Cape Town, South Africa", "Moscow, Russia", "São Paulo, Brazil",
    "Toronto, Canada", "Mexico City, Mexico", "Seoul, South Korea", "Bangkok, Thailand"
]

# 生成 200 条合成数据
synthetic_data = []
for i in range(5000):
    location = random.choice(locations)
    variable = random.choice(soil_variables)

    # 生成用户问题
    question = f"What is the {variable} content in {location}?"

    # 生成 JSON 结构的答案
    function_call = {
        "function": "get_soil_data",
        "parameters": {
            "location": location,
            "variable": variable
        }
    }

    # 存入数据列表
    synthetic_data.append({
        "QUESTION.question": question,
        "ANSWER": json.dumps(function_call)  # 转换为 JSON 字符串格式
    })

# 转换为 DataFrame
synthetic_function_calling_df = pd.DataFrame(synthetic_data)

# 保存到本地文件
synthetic_function_calling_df.to_csv("synthetic_function_calling_train.csv", index=False)
print("✅ 训练数据已生成并保存在 synthetic_function_calling_train.csv")
