import requests
import json
from process_forum_threads import process_forum_threads_batch
from processor_utils import process_dialogue

forums = {"Bluetooth Low Energy": "297",
          "RA MCU": "256"}
forumIds = []
urls = [] 
pages_remaining = True
all_threads = []
page_counter = 0

headers = {
    "Rest-User-Token": "a2JzZ2FqdWVxZWxwOWdybmR0YWp4bWU6RGVsb2l0dGUgQVBJ",
    "Content-Type": "application/json",
}
params = {
    "PageSize": "100",
    "PageIndex": page_counter
}

final_dialogue_list = {"messages": []}
final_file_name = "Forum_Fine_Tuning_Dialogue.json"

### TODO - if debugging set to True
testing = False

community_data_parent_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/CommunityData"
for forum in forums.keys():
    page_counter = 0
    print(f"Processing forum: {forum}")
    forumId = forums[forum]
    forumIds.append(forumId)
    url = f"https://community.renesas.com/api.ashx/v2/forums/{forumId}/threads.json"
    print(f"\tProcessing URL: {url}")
    urls.append(url)

    # Can get a max of 100 threads per page
    while pages_remaining:
        try: 
            response = requests.get(url, headers=headers, params=params).json() # type: ignore
            all_threads.extend(response['Threads'])
            page_counter+=1
            
            params['PageIndex'] = page_counter
            print("Counter Progress", page_counter)
            # Testing
            if testing & (page_counter == 1):
                break
            if not len(response['Threads']) == 100:
                pages_remaining = False
        except:
            print("API request failed at: ", url)
    
    # Dump all files to JSON
    with open(f"{forum}.json","w+") as f:
        json.dump(all_threads,f,indent=4)
    # Process the aggregate threads
    thread_content = process_forum_threads_batch(all_threads)
    print("Begin to process the dialogue...")
    for thread in thread_content:
        processed_dialogue = process_dialogue(thread)
        final_dialogue_list['messages'].append(processed_dialogue)

    print("Done Processing Data!")

print(f"Writing to file: {final_file_name}")

file_path = community_data_parent_dir + "/" + final_file_name
with open(file_path, "w+") as f:
    json.dump(final_dialogue_list,f,indent=4)
# dbutils.fs.put(file_path, json_data, overwrite=True)
