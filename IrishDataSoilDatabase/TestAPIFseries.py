import requests
import pandas as pd
import time

# Reload the soil series CSV file
file_path = "irish_soil_series.csv"
df_series = pd.read_csv(file_path)

# Filter only "LIVE" soil series
# live_series = df_series[df_series['Live'] == 'LIVE']
# series_ids = live_series["National_Series_Id"].tolist()

series_ids = df_series["National_Series_Id"].tolist()
# Store results
basic_info_list = []

# Loop through each live series ID and fetch basic info
for series_id in series_ids:
    # series_id = "0500KK"
    # Use this instead of get_series_full.php
    # url = f"http://gis.teagasc.ie/soils/get_series.php?series_id={series_id}"
    url = f"http://gis.teagasc.ie/soils/get_series_full.php?series_code={series_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data["series_id"] = series_id  # Add ID for reference
        basic_info_list.append(data)
    except Exception as e:
        print(f"Failed to fetch series {series_id}: {e}")
    time.sleep(0.3)  # polite delay

# Convert to DataFrame
df_basic = pd.DataFrame(basic_info_list)

# Save to CSV
output_path = "soil_series_basic_info2.csv"
df_basic.to_csv(output_path, index=False)

output_path  # return path for download
