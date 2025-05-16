# import psycopg2
# import pandas as pd
#
#
#
# # PostgreSQL 数据库连接信息
# DB_NAME = "iso28258"
# DB_USER = "postgres"
# DB_PASSWORD = "890723"  # 请替换为您的 PostgreSQL 密码
# DB_HOST = "localhost"
# DB_PORT = "5432"
#
# # 连接数据库
# conn = psycopg2.connect(
#     dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
#     host=DB_HOST, port=DB_PORT
# )
# cursor = conn.cursor()
#
# # 获取所有 Schema
# cursor.execute("SELECT schema_name FROM information_schema.schemata;")
# schemas = cursor.fetchall()
# df_schemas = pd.DataFrame(schemas, columns=["Schema"])
# tools.display_dataframe_to_user(name="数据库 Schemas", dataframe=df_schemas)
#
# # 获取所有表
# cursor.execute("""
#     SELECT table_schema, table_name
#     FROM information_schema.tables
#     WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY table_schema, table_name;
# """)
# tables = cursor.fetchall()
# df_tables = pd.DataFrame(tables, columns=["Schema", "Table"])
# tools.display_dataframe_to_user(name="数据库 Tables", dataframe=df_tables)
#
# # 获取表的详细结构
# cursor.execute("""
#     SELECT table_schema, table_name, column_name, data_type, is_nullable
#     FROM information_schema.columns
#     WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY table_schema, table_name, ordinal_position;
# """)
# columns = cursor.fetchall()
# df_columns = pd.DataFrame(columns, columns=["Schema", "Table", "Column", "Type", "Nullable"])
# tools.display_dataframe_to_user(name="数据库 表结构", dataframe=df_columns)
#
# # 获取外键关系
# cursor.execute("""
#     SELECT conname AS constraint_name, conrelid::regclass AS table,
#            pg_get_constraintdef(oid) AS definition
#     FROM pg_constraint
#     WHERE contype = 'f'
#     ORDER BY conrelid::regclass::text;
# """)
# foreign_keys = cursor.fetchall()
# df_foreign_keys = pd.DataFrame(foreign_keys, columns=["Constraint", "Table", "Definition"])
# tools.display_dataframe_to_user(name="数据库 外键关系", dataframe=df_foreign_keys)
#
# # 获取索引信息
# cursor.execute("""
#     SELECT indexname, tablename, indexdef
#     FROM pg_indexes
#     WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY tablename;
# """)
# indexes = cursor.fetchall()
# df_indexes = pd.DataFrame(indexes, columns=["Index", "Table", "Definition"])
# tools.display_dataframe_to_user(name="数据库 索引", dataframe=df_indexes)
#
# # 关闭连接
# cursor.close()
# conn.close()
# import psycopg2
# import pandas as pd
#
# # PostgreSQL 数据库连接信息
# DB_NAME = "iso28258"
# DB_USER = "postgres"
# DB_PASSWORD = "890723"  # 请替换为您的 PostgreSQL 密码
# DB_HOST = "localhost"
# DB_PORT = "5432"
#
# # 连接数据库
# conn = psycopg2.connect(
#     dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
#     host=DB_HOST, port=DB_PORT
# )
# cursor = conn.cursor()
#
# # 获取所有 Schema
# cursor.execute("SELECT schema_name FROM information_schema.schemata;")
# schemas = cursor.fetchall()
# df_schemas = pd.DataFrame(schemas, columns=["Schema"])
# print("\n📂 数据库 Schemas：")
# print(df_schemas)
#
# # 获取所有表
# cursor.execute("""
#     SELECT table_schema, table_name
#     FROM information_schema.tables
#     WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY table_schema, table_name;
# """)
# tables = cursor.fetchall()
# df_tables = pd.DataFrame(tables, columns=["Schema", "Table"])
# print("\n📂 数据库 Tables：")
# print(df_tables)
#
# # 获取表的详细结构
# cursor.execute("""
#     SELECT table_schema, table_name, column_name, data_type, is_nullable
#     FROM information_schema.columns
#     WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY table_schema, table_name, ordinal_position;
# """)
# columns = cursor.fetchall()
# df_columns = pd.DataFrame(columns, columns=["Schema", "Table", "Column", "Type", "Nullable"])
# print("\n📂 数据库 表结构：")
# print(df_columns)
#
# # 获取外键关系
# cursor.execute("""
#     SELECT conname AS constraint_name, conrelid::regclass AS table,
#            pg_get_constraintdef(oid) AS definition
#     FROM pg_constraint
#     WHERE contype = 'f'
#     ORDER BY conrelid::regclass::text;
# """)
# foreign_keys = cursor.fetchall()
# df_foreign_keys = pd.DataFrame(foreign_keys, columns=["Constraint", "Table", "Definition"])
# print("\n📂 数据库 外键关系：")
# print(df_foreign_keys)
#
# # 获取索引信息
# cursor.execute("""
#     SELECT indexname, tablename, indexdef
#     FROM pg_indexes
#     WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
#     ORDER BY tablename;
# """)
# indexes = cursor.fetchall()
# df_indexes = pd.DataFrame(indexes, columns=["Index", "Table", "Definition"])
# print("\n📂 数据库 索引：")
# print(df_indexes)
#
# # 关闭连接
# cursor.close()
# conn.close()
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

# 获取所有表
cursor.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name;
""")
tables = cursor.fetchall()
df_tables = pd.DataFrame(tables, columns=["Schema", "Table"])

# 获取外键关系
cursor.execute("""
    SELECT conname AS constraint_name, conrelid::regclass AS table_name, 
           pg_get_constraintdef(oid) AS definition
    FROM pg_constraint
    WHERE contype = 'f'
    ORDER BY conrelid::regclass::text;
""")
foreign_keys = cursor.fetchall()
df_foreign_keys = pd.DataFrame(foreign_keys, columns=["Constraint", "Table", "Definition"])

# 关闭连接
cursor.close()
conn.close()

# 创建有向图
G = nx.DiGraph()

# 添加表作为节点
for _, row in df_tables.iterrows():
    schema_table = f"{row['Schema']}.{row['Table']}"
    G.add_node(schema_table, color="lightblue")

# 添加外键关系作为边
for _, row in df_foreign_keys.iterrows():
    table_name = row["Table"]
    definition = row["Definition"]

    # 解析外键定义，找到依赖的表
    if "REFERENCES" in definition:
        ref_table = definition.split("REFERENCES")[1].split("(")[0].strip()
        G.add_edge(table_name, ref_table, color="red")

# 获取节点和边的颜色
node_colors = [G.nodes[n]["color"] for n in G.nodes()]
edge_colors = [G.edges[e]["color"] for e in G.edges()]

# 绘制图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # 自动布局
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=3000, font_size=10, font_weight="bold", alpha=0.7, arrowsize=15)

plt.title("📌 ISO 28258 数据库表与外键关系图")
plt.show()
