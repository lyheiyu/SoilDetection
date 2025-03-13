import streamlit as st
import psycopg2
import pandas as pd

# 数据库连接函数
def get_db_connection():
    return psycopg2.connect(
        dbname="iso28258",
        user="postgres",
        password="890723",
        host="localhost",
        port="5432"
    )

# 查询数据库中所有表的结构
def fetch_table_structure():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'core'
        ORDER BY table_name;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# 查询数据库中的所有表
def fetch_all_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'core';
    """)
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return [table[0] for table in tables]

# 查询指定表的数据
def fetch_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM core.{table_name};")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return column_names, rows

# Streamlit 页面标题
st.title("WOSIS dataspace")

# 显示所有表
st.header("Dataset structure")
tables = fetch_all_tables()
selected_table = st.selectbox("Select table", tables)

# 显示表结构
table_structure = fetch_table_structure()
structure_df = pd.DataFrame(table_structure, columns=["Table Name", "Column Name", "Data Type"])
filtered_structure = structure_df[structure_df["Table Name"] == selected_table]
st.dataframe(filtered_structure)

# 显示表数据
st.header("📊 Data display")
columns, data = fetch_table_data(selected_table)
data_df = pd.DataFrame(data, columns=columns)
st.dataframe(data_df)
