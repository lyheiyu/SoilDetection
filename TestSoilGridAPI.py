import requests
import pandas as pd
import csv
# Define the API endpoint and parameters
url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
params = {"lon": 10, "lat": 50}

# Make the request
response = requests.get(url, params=params)

# Check the response
if response.status_code == 200:
    print(response.json())
# covert the json to csv


else:
    print("Error:", response.status_code)
import json


# Example JSON data
# data = {
#     'type': 'Feature',
#     'geometry': {'type': 'Point', 'coordinates': [10.0, 50.0]},
#     'properties': {
#         'layers': [
#             {
#                 'name': 'bdod',
#                 'unit_measure': {'target_units': 'kg/dm³'},
#                 'depths': [
#                     {'label': '0-5cm', 'values': {'mean': 129, 'uncertainty': 6}},
#                     {'label': '5-15cm', 'values': {'mean': 135, 'uncertainty': 5}}
#                 ]
#             },
#             {
#                 'name': 'cec',
#                 'unit_measure': {'target_units': 'cmol(c)/kg'},
#                 'depths': [
#                     {'label': '0-5cm', 'values': {'mean': 282, 'uncertainty': 29}},
#                     {'label': '5-15cm', 'values': {'mean': 189, 'uncertainty': 28}}
#                 ]
#             }
#         ]
#     }
# }

# Define the output CSV file name
csv_file = "soil_data.csv"


#
# def print_tree(data, indent=0):
#     """
#     Recursively print JSON structure as a tree, combining same-level keys for simplicity.
#     """
#     if isinstance(data, dict):
#         same_level = []
#         for key, value in data.items():
#             if isinstance(value, (dict, list)):
#                 if same_level:
#                     print(" " * indent + f"- {', '.join(same_level)}")
#                     same_level = []
#                 print(" " * indent + f"- {key}:")
#                 print_tree(value, indent + 2)
#             else:
#                 same_level.append(f"{key}: {value}")
#         if same_level:
#             print(" " * indent + f"- {', '.join(same_level)}")
#     elif isinstance(data, list):
#         for index, item in enumerate(data):
#             print(" " * indent + f"- [{index}]:")
#             print_tree(item, indent + 2)
#     else:
#         print(" " * indent + f"{data}")
# print_tree(response.json())

# # Extract and write data to the CSV file
# def convert_json_to_csv(data, csv_file):
#     headers = ['Layer', 'Depth', 'Mean Value', 'Uncertainty', 'Units']
#     rows = []
#
#     # Extract data from the JSON
#     for layer in data['properties']['layers']:
#         layer_name = layer['name']
#         unit = layer['unit_measure']['target_units']
#         for depth in layer['depths']:
#             depth_label = depth['label']
#             mean = depth['values']['mean']
#             uncertainty = depth['values']['uncertainty']
#             rows.append([layer_name, depth_label, mean, uncertainty, unit])
#
#     # Write data to CSV
#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(rows)
#
#     print(f"Data successfully written to {csv_file}")
#
#
# # Convert the JSON data to CSV
# convert_json_to_csv(response.json(), csv_file)
def flatten_geojson_like(data):
    """
    GeoJSON to a table，each elment to a dict，including the csv。
    """
    # initiate a table
    all_rows = []

    # get the coordinates
    geometry = data.get("geometry", {})
    coords = geometry.get("coordinates", [])
    if len(coords) >= 2:
        lon, lat = coords[0], coords[1]
    else:
        lon, lat = None, None

    # 2. get layers
    properties = data.get("properties", {})
    layers = properties.get("layers", [])

    for layer in layers:
        #  get each layer information
        layer_name = layer.get("name")
        unit_measure = layer.get("unit_measure", {})
        mapped_units = unit_measure.get("mapped_units")
        target_units = unit_measure.get("target_units")
        d_factor = unit_measure.get("d_factor")
        uncertainty_unit = unit_measure.get("uncertainty_unit")

        # depth list
        depths = layer.get("depths", [])
        for depth_obj in depths:
            depth_range = depth_obj.get("range", {})
            label = depth_obj.get("label")  # e.g. '0-5cm'
            top_depth = depth_range.get("top_depth")
            bottom_depth = depth_range.get("bottom_depth")
            unit_depth = depth_range.get("unit_depth")

            values = depth_obj.get("values", {})
            # 这里 values 里常见的字段有 Q0.05, Q0.5, Q0.95, mean, uncertainty
            q005 = values.get("Q0.05")
            q05 = values.get("Q0.5")
            q095 = values.get("Q0.95")
            mean_val = values.get("mean")
            uncertainty = values.get("uncertainty")

            # 3. 组装一行扁平化数据(字典)
            row_dict = {
                "longitude": lon,
                "latitude": lat,
                "layer_name": layer_name,
                "mapped_units": mapped_units,
                "target_units": target_units,
                "d_factor": d_factor,
                "uncertainty_unit": uncertainty_unit,

                "depth_label": label,
                "top_depth": top_depth,
                "bottom_depth": bottom_depth,
                "unit_depth": unit_depth,

                "Q0.05": q005,
                "Q0.5": q05,
                "Q0.95": q095,
                "mean": mean_val,
                "uncertainty": uncertainty
            }

            # 如果想把 layer 本身的全部字段或 unit_measure 的全部字段加进去，也可以:
            # row_dict.update(layer)  # 这样会把 layer 的所有 key 覆盖到 row_dict 中
            # row_dict.update(unit_measure)

            # 收集到列表中
            all_rows.append(row_dict)

    return all_rows


def write_csv_from_rows(rows, output_csv_path, extra_fields=None):
    """
    给定一个列表(rows)，其中每个元素都是一个 dict。
    自动收集所有字段(列名)，并写入 CSV。
    extra_fields 可以额外手动指定表头的排列顺序或补充顺序。
    """
    # 1. 收集全部列名(自动)
    all_keys = set()
    for r in rows:
        all_keys.update(r.keys())
    # 如果需要保证某些固定字段顺序，可以将它们放在 extra_fields 前面
    # 剩余字段按字母排序(也可以自定义)
    if extra_fields is None:
        extra_fields = []
    all_keys = list(all_keys)
    # 去重的同时，把 extra_fields 放前面, 再拼接剩余的
    fieldnames = extra_fields + [k for k in all_keys if k not in extra_fields]

    # 2. 写入 CSV
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"write to CSV : {output_csv_path}")
data=response.json()
rows = flatten_geojson_like(data)


    # make the specific colums in front extra_fields
extra_fields = ["longitude", "latitude", "layer_name", "depth_label"]
write_csv_from_rows(rows, "output.csv", extra_fields=extra_fields)
# write_csv_from_rows(rows, "output.csv")