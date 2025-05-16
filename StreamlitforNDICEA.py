import streamlit as st
import requests

# Function to get access token
def get_token(username, password):
    url = "https://ndiceaweb.eu/api/RequestToken"
    headers = {"Content-Type": "application/json"}
    data = {"UserName": username, "Password": password}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("AccessToken")
    else:
        st.error(f"Failed to get token: {response.status_code}")
        return None

# Function to get regions
def get_regions(token):
    url = "https://ndiceaweb.eu/api/Scenario/GetAvailableRegions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch regions: {response.status_code}")
        return []

# Streamlit interface
st.title("NDICEA API Integration")
username = st.text_input("Enter your NDICEA username:")
password = st.text_input("Enter your NDICEA password:", type="password")

if st.button("Get Available Regions"):
    token = get_token(username, password)
    if token:
        regions = get_regions(token)
        st.success("Regions fetched successfully!")
        for region in regions:
            st.write(f"{region['Id']}: {region['NameEn']}")
