import requests
import json
import pandas as pd

url = "https://api.doge.gov/savings/grants?sort_by=date&sort_order=desc&page=1&per_page=100"

headers = {"accespt": "application/json" }
response = requests.get(url , 
                        headers=headers)

# make the GET request to the API endpoint
if response.status_code == 200:
    data = response.json()

    # Extract the list of grants
    grants = data["result"]["grants"]

# Convert to DataFrame
    df = pd.DataFrame(grants)

# Optionally display
    print(df.head())

    # print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")