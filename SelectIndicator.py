import streamlit as st
import pandas as pd
import sqlite3

# 数据库路径
db_path = "soil_indicators.db"

# **连接数据库并获取数据**
def load_data():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM indicators", conn)
    conn.close()
    return df

# **确保数据库和表存在**
def ensure_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Indicator TEXT,
            Unit_of_Measurement TEXT,
            Description TEXT,
            NL TEXT,
            SP TEXT,
            IR TEXT,
            FR TEXT
        )
    ''')
    conn.commit()
    conn.close()

ensure_database()

# **加载数据**
data = load_data()

# **自动检测国家列**
def separate_columns(df):
    fixed_columns = {"id", "Category", "Indicator", "Unit of Measurement", "Description"}
    country_columns = [col for col in df.columns if col not in fixed_columns]
    return country_columns, list(fixed_columns)

# 获取国家列 & 其他列
country_columns, fixed_columns = separate_columns(data)

# **用户选择国家**
countries = st.multiselect("Select Countries", country_columns, default=country_columns)

# **选择指标分类**
categories = ["All"] + list(data["Category"].dropna().unique())
category = st.selectbox("Select Category", categories)

# **搜索栏**
search_query = st.text_input("Search Indicator")

# **数据筛选**
def filter_data(df, countries, category, search_query):
    filtered_df = df.copy()

    # **确保所有数据都是字符串，并转换为小写，忽略 "X" 和 "x" 的大小写差异**
    df[countries] = df[countries].fillna("").astype(str).apply(lambda x: x.str.lower())

    # **按国家筛选**
    if countries:
        if len(countries) == 1:
            country_filter = df[countries[0]] == "x"
        else:
            country_filter = df[countries].eq("x").all(axis=1)
        filtered_df = filtered_df[country_filter]

    # **按类别筛选**
    if category and category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category]

    # **按关键词搜索**
    if search_query:
        filtered_df = filtered_df[filtered_df["Indicator"].str.contains(search_query, case=False, na=False)]

    return filtered_df

# **应用筛选**
filtered_data = filter_data(data, countries, category, search_query)

# **显示数据（可编辑）**
st.subheader("Edit Data Directly")

edited_data = st.data_editor(filtered_data, num_rows="dynamic")

# **保存修改**
if st.button("Save Changes"):
    conn = sqlite3.connect(db_path)
    edited_data.to_sql("indicators", conn, if_exists="replace", index=False)
    conn.close()
    st.success("Database updated successfully!")

# **数据导出**
st.download_button("Download CSV", filtered_data.to_csv(index=False), "filtered_data.csv", "text/csv")

# **新增国家列**
st.subheader("Add New Country")

new_country = st.text_input("Enter New Country Code (e.g., DE, IT)")

if st.button("Add Country"):
    if new_country and new_country.isidentifier() and new_country not in country_columns:
        conn = sqlite3.connect(db_path)
        try:
            # **添加新国家列**
            conn.execute(f"ALTER TABLE indicators ADD COLUMN '{new_country}' TEXT;")
            conn.commit()

            # **为所有现有数据填充默认值**
            data[new_country] = ""  # 默认值为空（国家不能做此指标）
            data.to_sql("indicators", conn, if_exists="replace", index=False)

            st.success(f"Country '{new_country}' added successfully!")
        except Exception as e:
            st.error(f"Failed to add country: {e}")
        finally:
            conn.close()
        st.experimental_rerun()
    else:
        st.warning("Invalid country code or country already exists.")

# **新增数据**
st.subheader("Add New Data")

new_data = {}
for col in fixed_columns + country_columns:
    new_data[col] = st.text_input(f"Enter {col}")

if st.button("Add Row"):
    conn = sqlite3.connect(db_path)
    placeholders = ", ".join(["?" for _ in new_data])
    conn.execute(f"INSERT INTO indicators ({', '.join(new_data.keys())}) VALUES ({placeholders})", tuple(new_data.values()))
    conn.commit()
    conn.close()
    st.success("New row added!")
