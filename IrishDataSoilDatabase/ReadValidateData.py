import pandas as pd
import ast

# 读取你的原始 Excel 或 CSV 文件
# df = pd.read_excel('your_file.xlsx')  # 或 pd.read_csv('your_file.csv')
df=pd.read_csv('soil_series_basic_info2.csv')
# 用于存放清洗后的所有 horizon 条目
cleaned_data = []

for idx, row in df.iterrows():
    series_id = row['series_id']
    try:
        horizons = ast.literal_eval(row['Horizons'])  # 转换字符串为 list
    except (ValueError, SyntaxError):
        continue  # 如果无法解析，就跳过

    # 跳过空列表
    if not horizons or not isinstance(horizons, list):

        continue

    for horizon in horizons:
        if isinstance(horizon, dict):
            # 删除 None 值字段
            cleaned_horizon = {k: v for k, v in horizon.items() if v is not None}
            if cleaned_horizon:
                cleaned_horizon['series_id'] = series_id  # 添加对应 series_id
                cleaned_data.append(cleaned_horizon)

# 转换为 DataFrame
cleaned_df = pd.DataFrame(cleaned_data)

# 保存为 CSV 文件
cleaned_df.to_csv('cleaned_horizons_per_series_id.csv', index=False)
print("清洗完成，保存为 cleaned_horizons_per_series_id.csv")
