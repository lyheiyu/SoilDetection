import os
import psycopg2

# PostgreSQL 数据库连接配置
DB_NAME = "iso28258"
DB_USER = "postgres"
DB_PASSWORD = "890723"  # 请输入您的 PostgreSQL 密码
DB_HOST = "localhost"
DB_PORT = "5432"

# SQL 文件所在的目录（请修改为实际路径）
MIGRATIONS_DIR = "./migrations/committed"


def execute_sql_file(cursor, filepath):
    """执行单个 SQL 文件"""
    with open(filepath, "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()
        cursor.execute(sql_script)


def run_migrations():
    """批量执行 SQL 迁移文件"""
    try:
        # 连接到 PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
            host=DB_HOST, port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # 获取并按文件名排序 SQL 迁移文件
        sql_files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")])

        print(f"📂 发现 {len(sql_files)} 个 SQL 迁移文件，即将执行...")

        # 逐个执行 SQL 文件
        for sql_file in sql_files:
            filepath = os.path.join(MIGRATIONS_DIR, sql_file)
            print(f"🚀 正在执行: {sql_file}")
            execute_sql_file(cursor, filepath)

        # 关闭数据库连接
        cursor.close()
        conn.close()
        print("✅ 所有 SQL 迁移文件已成功执行！")

    except Exception as e:
        print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    run_migrations()
