import requests

ACCESS_TOKEN = "Bp7fXzYmuchum9Rge3PzyfuIXAfijzgHAhr8buMD2VdnfOhIK9gBCFIoi98b"

# 1. 创建一个新的草稿记录
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
r = requests.post("https://zenodo.org/api/deposit/depositions", headers=headers, json={})
deposition_id = r.json()["id"]
print(f"Created deposition ID: {deposition_id}")

# 2. 上传文件
files = {'file': open('file/qna-dataset-farmgenie-soil-v2.csv', 'rb')}
r = requests.post(
    f"https://zenodo.org/api/deposit/depositions/{deposition_id}/files",
    headers=headers,
    data={'name': 'qna-dataset-farmgenie-soil-v2.csv'},
    files=files
)

# 3. 添加 metadata
metadata = {
    "metadata": {

    "creators": [
        {
            "name": "Xinyu Yan",
            "affiliation": "Technological University of the Shannon, Software Research Institute",
            "type": "ProjectMember"
        }
    ],
    "contributors": [
        {
            "name": "Technological University of the Shannon",
            "type": "HostingInstitution"
        }
    ],
    "title": "SOILCRATES Soil Health Dataset",
    "version": "1.0.0",
    "access_right": "open",
    "related_identifiers": [
        {
            "identifier": "https://github.com/xinyuyan/soilcrates-soil-health",
            "relation": "isSupplementTo",
            "resource_type": "software"
        }
    ],
    "keywords": [
        "soil health",
        "FTIR",
        "ISO28258",
        "INSPIRE",
        "GloSIS",
        "Ireland",
        "dataset"
    ],
    "license": "CC-BY-4.0",
    "upload_type": "dataset",
    "language": "eng",

    "description": "Test version"

    }
}

r = requests.put(
    f"https://zenodo.org/api/deposit/depositions/{deposition_id}",
    headers=headers,
    json=metadata
)
print("Metadata updated!")

# 4. 发布
r = requests.post(
    f"https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish",
    headers=headers
)
print("Published! DOI:", r.json()["doi"])
