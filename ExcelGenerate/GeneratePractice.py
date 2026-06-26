from openpyxl import Workbook

files = [
"SOILCRATES Practice Sheets_01-reduced and non inversion tillage_fin.xlsx",
"SOILCRATES Practice Sheets_02-Buffer zone strips_fin.xlsx",
"SOILCRATES Practice Sheets_03-Agroforestry_fin.xlsx",
"SOILCRATES Practice Sheets_04-Diversified crop rotation_fin.xlsx",
"SOILCRATES Practice Sheets_05-Strip cropping_fin.xlsx",
"SOILCRATES Practice Sheets_06a-Cover crops for carbon_fin.xlsx",
"SOILCRATES Practice Sheets_06b-Cover crops for nitrogen_fin.xlsx",
"SOILCRATES Practice Sheets_06c-Catch crops to reduce nitrog_fin.xlsx",
"SOILCRATES Practice Sheets_06d-Cover crops in the rotation_fin.xlsx",
"SOILCRATES Practice Sheets_07-Intercropping_fin.xlsx",
"SOILCRATES Practice Sheets_08-Tagetes for nematode control_fin.xlsx",
"SOILCRATES Practice Sheets_09- Species diversification_fin.xlsx",
"SOILCRATES Practice Sheets_10-compost_fin.xlsx",
"SOILCRATES Practice Sheets_11-bokashi_fin.xlsx",
"SOILCRATES Practice Sheets_12-biochar_fin.xlsx",
"SOILCRATES Practice Sheets_13-seaweed products_fin.xlsx",
"SOILCRATES Practice Sheets_14-digestate_fin.xlsx",
"SOILCRATES Practice Sheets_15-clay minerals_fin.xlsx",
"SOILCRATES Practice Sheets_16-wood ash_fin.xlsx",
"SOILCRATES Practice Sheets_17-gypsum-for-soil-structure_fin.xlsx",
"SOILCRATES Practice Sheets_18-microbial-biostimulants_fin.xlsx",
"SOILCRATES Practice Sheets_19-humic-products_fin.xlsx",
"SOILCRATES Practice Sheets_20-water-erosion-control_fin.xlsx",
"SOILCRATES Practice Sheets_21-wind erosion control_fin.xlsx",
"SOILCRATES Practice Sheets_22-low-pressure tyres_fin.xlsx",
"SOILCRATES Practice Sheets_23-deep-rooting crops_fin.xlsx",
"SOILCRATES Practice Sheets_24-perennial crops_fin.xlsx",
"SOILCRATES Practice Sheets_25-Phytoremediation_fin.xlsx",
"SOILCRATES Practice Sheets_26-field inundation_fin.xlsx",
"SOILCRATES Practice Sheets_27-Permanent grassland_fin.xlsx",
"SOILCRATES Practice Sheets_28-Integrated Crop Management_fin.xlsx",
"SOILCRATES Practice Sheets_29-Irrigation systems_fin.xlsx",
"SOILCRATES Practice Sheets_30-Water catchment infrastructure_fin.xlsx",
"SOILCRATES Practice Sheets_31-Man-made rills_fin.xlsx",
"SOILCRATES Practice Sheets_32-Soil decompaction measures_fin.xlsx"
]

wb = Workbook()
ws = wb.active
ws.title = "Practices"
ws.append(["Practice编号", "Practice名称", "原文件名"])

for f in files:
    core = f.replace("SOILCRATES Practice Sheets_", "").replace("_fin.xlsx", "")
    number, name = core.split("-", 1)
    ws.append([number, name.strip(), f])

path = "SOILCRATES_practice_list.xlsx"
wb.save(path)

