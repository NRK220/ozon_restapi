import requests
import json


host = 'https://api-seller.ozon.ru'
# endpoint = '/v2/products/stocks'
endpoint = '/v3/posting/fbs/unfulfilled/list'




headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Client-Id': '77277',
    'Api-Key': '6ff1c009-b044-4d3d-9bc2-fe3d12566f1b'
}

#body
payload = {
    "dir": "ASC",
    "filter": {
        "cutoff_from": "2024-06-03T14:15:22Z",
        "cutoff_to": "2024-06-16T14:15:22Z",
        "status": "awaiting_packaging"
    },
    "limit": 100
}


res = requests.post(host + endpoint, headers=headers, json=payload)


print(res.status_code)


if res.status_code == 200:
    # Parse and print the JSON data from the response
    json_data = res.json()
    print(json_data)
    # Save the JSON data to a file
    file_path = 'data.json'
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print("JSON data has been saved to data.json")
else:
    print(f"Failed to fetch data from API. Status code: {res.status_code}, Response: {res.text}")