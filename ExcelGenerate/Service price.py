from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "GPU_Comparison_Summary"

headers = [
    "Cloud Provider",
    "Instance Type",
    "GPU Type",
    "GPUs",
    "vCPUs",
    "Memory (GiB)",
    "Linux On-Demand (€ / month)",
    "Linux Spot (€ / month)",
    "Best Use Case",
    "Stability"
]

ws.append(headers)

rows = [
    ["AWS", "g5.xlarge", "A10G", 1, 4, 16, 704.79, 444.02, "Platform + small model inference", "High"],
    ["AWS", "g5.2xlarge", "A10G", 1, 8, 32, 849.12, 588.44, "Platform + inference", "High"],
    ["GCP", "A2 Highgpu 1g", "A100", 1, 12, 85, 522.66, 196.47, "Training / inference (Spot)", "Low (Spot)"],
    ["GCP", "A2 Highgpu 2g", "A100", 2, 24, 170, 1045.32, 392.93, "Multi-GPU training", "Low (Spot)"],
    ["Azure", "NC16ads A10 v4", "A10", 1, 16, 220, 1794.93, 331.70, "Enterprise GPU workloads", "Medium"],
    ["Azure", "NC24ads A100 v4", "A100", 1, 24, 220, 2996.78, 1380.62, "HPC / Training", "Medium"]
]

for r in rows:
    ws.append(r)

path = "GPU_Cloud_Comparison.xlsx"
wb.save(path)

path
