import pandas as pd
import sqlite3

# 读取 Excel 文件
file_path = "forDatabase.xlsx"
df = pd.read_excel(file_path)

# 连接 SQLite 数据库
db_path = "soil_indicators.db"
conn = sqlite3.connect(db_path)

# 存入数据库
df.to_sql("indicators", conn, if_exists="replace", index=False)

# 关闭连接
conn.close()

# 返回数据库文件路径，用户可以下载
db_path
