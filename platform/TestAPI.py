import requests

response = requests.post(
    "http://localhost:3000/workpackages",
    json={
        # "id": "2",
        "name": "WP1_Living_Labs",
        "description": "Living lab for testing1"
    }
)

print(response.status_code)
print(response.json())
