import requests
import json
import pandas as pd
# # Use a valid association unit ID (from your doc: 0600a or 0300a)
# assoc_id = "0600a"
# url = f"http://gis.teagasc.ie/soils/services//get_all_associations.php"
#
#
# # Send request
# response = requests.get(url)
#
# # Check status
# if response.status_code == 200:
#     data = response.json()
#     print(json.dumps(data, indent=2))  # Pretty print
#
#     df = pd.DataFrame(data)
#
#     # Save to CSV
#     df.to_csv("irish_soil_associations.csv", index=False)
# else:
#     print(f"Failed to fetch data: {response.status_code}")
assoc_id = "0600a"
url = f"http://gis.teagasc.ie/soils/get_associations.php?assoc_id=0600a "

# Send request
response = requests.get(url)
print(response.text)
# Check status
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))  # Pretty print

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv("irish_soil_associations.csv", index=False)
else:
    print(f"Failed to fetch data: {response.status_code}")