import requests
import json
from process_forum_threads import process_forum_threads_batch

url = f"https://community.renesas.com/api.ashx/v2/forums/{forumId}/threads.json"

forums = {"Bluetooth Low Energy": "297",
          "RA MCU": "256"}
forumIds = []
urls = [] 
headers = {
    "Rest-User-Token": "a2JzZ2FqdWVxZWxwOWdybmR0YWp4bWU6RGVsb2l0dGUgQVBJ",
    "Content-Type": "application/json",
}
params = {
    "PageSize": "100",
    "PageIndex": "0"
}
community_data_parent_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/CommunityData"
for forum in forums.keys():
    print(f"Processing forum: {forum}")
    forumId = forums[forum]
    forumIds.append(forumId)
    url = f"https://community.renesas.com/api.ashx/v2/forums/{forumId}/threads.json"
    print(f"Processing URL: {url}")
    urls.append(url)
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        json_data = response.json()
        with open(f"{forum}.json","w+") as f:
            json.dump(json_data,f,indent=4)
        process_forum_threads_batch(json_data)
    else:
        print("API request failed with status code:", response.status_code)