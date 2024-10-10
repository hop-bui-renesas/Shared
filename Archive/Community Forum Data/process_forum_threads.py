from concurrent.futures import ThreadPoolExecutor
import math
from process_replies_thread import process_replies_given_thread

num_workers = 8
def process_forum_threads_single_batch(thread_batch):
    batch_replies = []
    #for each thread in thread_batch, get the url and then send the request to process_replies_given_thread
    for thread in thread_batch:
        process_replies_given_thread
    return batch_replies
def process_forum_threads_batch(threads):
    #Split threads into Worker Batches
    batch_size = math.ceil(len(threads)/num_workers)
    #create batches of utmost batch_size, which is list of lists
    forum_thread_batches_list = [] 
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        batch_replies_list = list(executor.map(process_forum_threads_single_batch,forum_thread_batches_list))
    all_replies = []
    for batch in batch_replies_list:
        for replies in batch:
            all_replies.extend(replies)
    return all_replies
    

