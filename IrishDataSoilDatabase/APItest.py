import requests
import pandas as pd

# URL to fetch soil series data
url = "http://gis.teagasc.ie/soils/services/get_all_series.php"
# url = "https://gis.teagasc.ie/services/get_all_series.php"

# Send the request
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad responses

# Load JSON into DataFrame
data = response.json()
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("irish_soil_series.csv", index=False)

print("Data saved to 'irish_soil_series.csv'")

# import time
#
# # Read CSV of soil series
# df_series = pd.read_csv("irish_soil_series.csv")
#
# # Get the first 10 series codes
# series_ids = df_series["National_Series_Id"].head(10).tolist()
#
# # List to hold full details for each series
# detailed_data = []
#
# # Loop over each series ID and fetch full detail
#
#
# for series_id in series_ids:
#     url = f"http://gis.teagasc.ie/soils/services/get_series.php?series_id={series_id}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise error for HTTP issues
#         data = response.json()
#
#         if isinstance(data, dict):
#             data["series_code"] = series_id  # Attach series ID for reference
#             detailed_data.append(data)
#     except Exception as e:
#         print(f"Failed to fetch series {series_id}: {e}")
#
#     time.sleep(0.5)  # Delay to avoid spamming the server
#
# # Extract relevant fields from full JSON into a summary table
# summary_list = [
#     {
#         "series_code": item.get("series_code"),
#         "series_name": item.get("series", {}).get("Series_Name"),
#         "description": item.get("series", {}).get("Series_Description"),
#         "texture": item.get("series", {}).get("Series_Texture"),
#         "drainage": item.get("series", {}).get("Series_Drainage"),
#     }
#     for item in detailed_data
# ]
#
# # Convert to DataFrame and preview
# df_detail = pd.DataFrame(summary_list)
# df_detail.to_csv("soil_series_full_details.csv", index=False)
# print("Saved detailed summary to 'soil_series_full_details.csv'")

