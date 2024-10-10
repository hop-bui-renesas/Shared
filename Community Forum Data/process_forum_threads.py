from concurrent.futures import ThreadPoolExecutor
import math
from process_replies_thread import process_replies_given_thread
from tqdm import tqdm

num_workers = 8

def batch_generator(data, batch_size):
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def process_forum_threads_single_batch(thread_batch):
    batch_threads_and_replies = []
    #for each thread in thread_batch, get the url and then send the request to process_replies_given_thread
    for thread in thread_batch:
        # Extract thread information needed
        content_id = thread['ContentId']
        subject = thread['Subject']
        body = thread['Body']
        author_id = thread['Author']['Id']
        thread_id = thread['Id']
        forum_id = thread['ForumId']

        # Extract the thread id from the JSON
        
        response_url = f"https://community.renesas.com/api.ashx/v2/forums/{forum_id}/threads/{thread_id}/replies.json"
        thread_replies = process_replies_given_thread(get_url=response_url)

        # combine the Thread and its replies
        thread_and_reply = {"ContentId": content_id, 
                            "Subject": subject, 
                            "Body": body, 
                            "AuthorId": author_id, 
                            "Replies": thread_replies,
                            "ThreadId": thread_id}
        batch_threads_and_replies.append(thread_and_reply)

    return batch_threads_and_replies

def process_forum_threads_batch(threads):
    print("Beginning to process threads...")
    #Split threads into Worker Batches
    batch_size = math.ceil(len(threads)/num_workers)
    #create batches of utmost batch_size, which is list of lists
    forum_thread_batches_list = []
    for batch in batch_generator(threads, batch_size):
        # Process each batch
        forum_thread_batches_list.append(batch)

    # Spread processing across workers in batches    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        batch_replies_list = list(tqdm(executor.map(process_forum_threads_single_batch, forum_thread_batches_list)))
    
    print("Batch Processing Completed...")
    # combine all threads into a single list (Thread body and replies included)
    all_content = []
    for batch in batch_replies_list:
        for replies in batch:
            all_content.append(replies)
    return all_content