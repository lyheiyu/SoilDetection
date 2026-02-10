# merge_soil_data.py
import pandas as pd
from pathlib import Path

def build_fact_tables(base_dir: str):
    base = Path(base_dir)

    # 1. 读取基础设计表（假设 StudyDesign.xlsx 里面有一张 Master_Plot_Design 表）
    study = pd.read_excel(base / "SoilC.xlsx", sheet_name="Master_Plot_Design")

    # 2. 读取采样事件
    events = pd.read_excel(base / "SamplingEvents.xlsx", sheet_name="SamplingEvents")

    # 3. 读取土壤测量宽表
    meas = pd.read_excel(base / "SoilMeasurements.xlsx", sheet_name="SoilMeasurements")

    # === 这里字段名你后面可以根据你真实列名微调 ===
    # 假设：
    #   StudyDesign: Project_ID, Experiment_ID, Plot_ID, Treatment_No
    #   events: Plot_ID, Event_ID, Event_Date, Weather_Condition, Temperature_Class, Rainfall_LastWeek
    #   meas: Plot_ID, Event_ID, Sample_ID, pH_H2O, SOC_gkg, TN_gkg, AvP_mgkg, AvK_mgkg, EC_dSm, BulkDensity_gcm3

    # 4. 合并：测量 + 设计信息（按 Plot_ID）
    fact = meas.merge(
        study[["Project_ID", "Experiment_ID", "Plot_ID", "Treatment_No"]],
        on="Plot_ID",
        how="left",
        validate="m:1"   # 多个测量对应一个 Plot
    )

    # 5. 再合并：采样事件（Plot_ID + Event_ID）
    fact = fact.merge(
        events[["Plot_ID", "Event_ID", "Event_Date",
                "Weather_Condition", "Temperature_Class", "Rainfall_LastWeek"]],
        on=["Plot_ID", "Event_ID"],
        how="left",
        validate="m:1"
    )

    # 6. 简单质量检查
    missing_design = fact[fact["Experiment_ID"].isna()]
    missing_event = fact[fact["Event_Date"].isna()]

    # 7. 导出宽表结果
    fact_out = base / "Fact_SoilMeasurements.xlsx"
    fact.to_excel(fact_out, index=False)

    # 8. 生成 O&M 风格长表
    long_rows = []
    property_cols = [
        ("pH_H2O",      "PH_H2O",    "pH"),
        ("SOC_gkg",     "SOC_GKG",   "g/kg"),
        ("TN_gkg",      "TN_GKG",    "g/kg"),
        ("AvP_mgkg",    "AVP_MGKG",  "mg/kg"),
        ("AvK_mgkg",    "AVK_MGKG",  "mg/kg"),
        ("EC_dSm",      "EC_DSM",    "dS/m"),
        ("BulkDensity_gcm3", "BD_GCM3", "g/cm3"),
        # 你可以在这里继续加更多属性列
    ]

    for _, row in fact.iterrows():
        for col_name, prop_code, unit_code in property_cols:
            value = row.get(col_name)
            if pd.isna(value):
                continue
            long_rows.append({
                "Project_ID": row["Project_ID"],
                "Experiment_ID": row["Experiment_ID"],
                "Plot_ID": row["Plot_ID"],
                "Sample_ID": row.get("Sample_ID"),
                "Event_ID": row["Event_ID"],
                "Event_Date": row["Event_Date"],
                "Property_Code": prop_code,
                "Value_Numeric": value,
                "Unit_Code": unit_code,
                "Weather_Condition": row["Weather_Condition"],
                "Rainfall_LastWeek": row["Rainfall_LastWeek"],
            })

    long_df = pd.DataFrame(long_rows)
    long_out = base / "SoilMeasurements_Long.csv"
    long_df.to_csv(long_out, index=False)

    # 9. QA 报告
    qa_path = base / "QA_Report.xlsx"
    with pd.ExcelWriter(qa_path) as writer:
        missing_design.to_excel(writer, sheet_name="Missing_Design", index=False)
        missing_event.to_excel(writer, sheet_name="Missing_Events", index=False)

    # 返回一些摘要信息给 GUI 展示
    summary = {
        "n_fact_rows": len(fact),
        "n_missing_design": len(missing_design),
        "n_missing_event": len(missing_event)
    }

    return {
        "fact_path": str(fact_out),
        "long_path": str(long_out),
        "qa_path": str(qa_path),
        "summary": summary
    }
