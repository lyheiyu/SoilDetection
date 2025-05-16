import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# PostgreSQL 数据库连接信息
DB_NAME = "iso28258"
DB_USER = "postgres"
DB_PASSWORD = "890723"  # 请替换为您的 PostgreSQL 密码
DB_HOST = "localhost"
DB_PORT = "5432"

# 连接数据库
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
    host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# # 获取所有表
# cursor.execute("""
#     SELECT table_schema, table_name
#     FROM information_schema.tables
#     WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY table_schema, table_name;
# """)
# tables = cursor.fetchall()
# df_tables = pd.DataFrame(tables, columns=["Schema", "Table"])

cursor.execute("""
    SELECT * FROM core.property_phys_chem;
""")

data = cursor.fetchall()
data=pd.DataFrame(data)
data.to_csv('property_phys_chem.csv')
# use pandas to savdae the data to csv or xls




#
