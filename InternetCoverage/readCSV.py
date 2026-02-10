import os
import pandas as pd

# ===== 1. 配置：你的“空文件+文件名是数据”的文件夹 =====
FOLDER = r"272-Ireland.csv"  # 改成你的目录

OUTPUT_DIR = r"C:\D\projects\SoilDetection\SoilDetection\InternetCoverage"
IRELAND_CSV = os.path.join(OUTPUT_DIR, "ireland_from_filenames.csv")
LIMERICK_CSV = os.path.join(OUTPUT_DIR, "limerick_from_filenames.csv")

# Limerick 大致范围
LAT_MIN, LAT_MAX = 52.5, 52.8
LON_MIN, LON_MAX = -8.8, -8.4

# OpenCelliD cell_towers 格式列名
COLUMNS = [
    "radio",        # GSM / UMTS / LTE / NR
    "mcc",          # 272 = Ireland
    "mnc",          # 1 Vodafone, 3 Eir, 2/5 Three
    "lac_tac",      # LAC/TAC
    "cid",          # Cell ID
    "psc_pci",      # PSC/PCI 或 -1
    "lon",          # 经度
    "lat",          # 纬度
    "range",        # 估计覆盖半径
    "samples",      # 测量次数
    "changeable",   # 0/1
    "created",      # 首次出现时间戳
    "updated",      # 最近出现时间戳
    "avg_signal"    # 平均信号
]

rows = []

for fname in os.listdir(FOLDER):
    full_path = os.path.join(FOLDER, fname)
    if not os.path.isfile(full_path):
        continue  # 跳过子文件夹

    # 关键修改：不要再用 splitext 砍掉小数点后面的内容
    name_without_ext = fname.strip()  # 防止首尾空格

    parts = name_without_ext.split(",")

    if len(parts) != len(COLUMNS):
        print(
            f"Skipping '{fname}' because it has {len(parts)} fields, "
            f"expected {len(COLUMNS)}"
        )
        continue

    rows.append(parts)

print(f"Parsed {len(rows)} rows from filenames.")

# 构建 DataFrame
df = pd.DataFrame(rows, columns=COLUMNS)

# 转数值列
numeric_cols = [
    "mcc", "mnc", "lac_tac", "cid", "psc_pci",
    "lon", "lat", "range", "samples",
    "changeable", "created", "updated", "avg_signal"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nHead of parsed DataFrame:")
print(df.head())
print("Shape:", df.shape)

# ===== 2. 添加运营商和网络制式 =====

def operator_from_mnc(mnc):
    try:
        m = int(mnc)
    except Exception:
        return "Unknown"
    if m == 1:
        return "Vodafone"
    elif m == 3:
        return "Eir"
    elif m in (2, 5):
        return "Three"
    return f"Other_{m}"

df["operator"] = df["mnc"].apply(operator_from_mnc)

tech_map = {"GSM": "2G", "UMTS": "3G", "LTE": "4G", "NR": "5G"}
df["tech"] = df["radio"].map(tech_map).fillna(df["radio"])

print("\nOperator counts (all data):")
print(df["operator"].value_counts())
print("\nTech counts (all data):")
print(df["tech"].value_counts())

# 保存完整数据
df.to_csv(IRELAND_CSV, index=False)
print(f"\nSaved full dataset to: {IRELAND_CSV}")

# ===== 3. Limerick 子集 =====

limerick = df[
    (df["lat"] >= LAT_MIN) & (df["lat"] <= LAT_MAX) &
    (df["lon"] >= LON_MIN) & (df["lon"] <= LON_MAX)
].copy()

print("\nLimerick rows:", limerick.shape[0])
if not limerick.empty:
    print(limerick[["operator", "tech", "lat", "lon"]].head())

    print("\nOperator counts in Limerick:")
    print(limerick["operator"].value_counts())

    print("\nTech counts in Limerick:")
    print(limerick["tech"].value_counts())

    limerick.to_csv(LIMERICK_CSV, index=False)
    print(f"\nSaved Limerick subset to: {LIMERICK_CSV}")
else:
    print("No rows found in current Limerick bbox.")

# ===== 4. 可选：画地图 =====
try:
    import folium

    if not limerick.empty:
        m = folium.Map(location=[52.66, -8.63], zoom_start=11)

        def color_for_operator(op):
            if op == "Vodafone":
                return "red"
            elif op == "Eir":
                return "green"
            elif op == "Three":
                return "blue"
            else:
                return "gray"

        for _, row in limerick.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=4,
                color=color_for_operator(row["operator"]),
                fill=True,
                fill_opacity=0.7,
                popup=f"{row['operator']} - {row['tech']} (cid={row['cid']})"
            ).add_to(m)

        html_path = os.path.join(OUTPUT_DIR, "limerick_from_filenames.html")
        m.save(html_path)
        print(f"\nSaved Limerick map to: {html_path}")
    else:
        print("\nSkip map generation: empty Limerick subset.")
except ImportError:
    print("\nfolium not installed, skipping map step. Install with: pip install folium")
