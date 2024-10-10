#Worker function to get the replies of a single thread in a particular forum
import requests
import json

def process_replies_given_thread(get_url):
    processed_replies = []
    page_counter = 0
    pages_remaining = True
    all_replies = []

    headers = {
        "Rest-User-Token": "a2JzZ2FqdWVxZWxwOWdybmR0YWp4bWU6RGVsb2l0dGUgQVBJ",
        "Content-Type": "application/json",
    }
    params = {
        "PageSize": "10",
        "PageIndex": page_counter
    }

    while pages_remaining:
        try: 
            response = requests.get(get_url, headers=headers, params=params).json()
            all_replies.extend(response['Replies'])
            page_counter+=1
            
            params['PageIndex'] = page_counter
            # Testing
            if not len(response['Replies']) == 100:
                pages_remaining = False
        except:
            print("API request failed at: ", get_url)
    
    # TODO - Process out the content needed from noise
    
    for reply in all_replies: 
        # Extract thread information needed
        content_id = reply['ContentId']
        subject = reply['Subject']
        body = reply['Body']
        author_id = reply['Author']['Id']
        reply_id = reply['Id']
        parent_id = reply['ParentId']

        processed_reply = {"ContentId": content_id, 
                            "Subject": subject, 
                            "Body": body, 
                            "AuthorId": author_id,
                            "ReplyId": reply_id,
                            "ParentId": parent_id}
        processed_replies.append(processed_reply)

    return processed_replies
