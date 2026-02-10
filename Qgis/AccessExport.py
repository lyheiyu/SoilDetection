import pandas as pd
import pyodbc

mdb_file = ('C:\D\projects\SoilDetection\SoilDetection\Qgis\SOTER_Danube_worked_example2021.mdb')  # 修改为你的路径
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={mdb_file};'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 查看所有表名
tables = [x.table_name for x in cursor.tables(tableType='TABLE')]
print("所有表名:", tables)

# 批量导出所有表为 CSV
for tablename in tables:
    print(f"正在导出表：{tablename}")
    df = pd.read_sql(f'SELECT * FROM [{tablename}]', conn)
    df.to_csv(f'{tablename}.csv', index=False, encoding='utf-8-sig')

conn.close()
print("全部导出完成！")
