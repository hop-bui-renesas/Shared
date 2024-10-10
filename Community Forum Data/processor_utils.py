# This file holds utility functions that assist in the processing of community data

import re
from bs4 import BeautifulSoup

def clean_body_text(body_text):
    """Removes HTML tags, handles breaks, and replaces link tags with src attributes while preserving link text."""

    soup = BeautifulSoup(body_text, "html.parser")

    for a_tag in soup.find_all("a"):
        image_link = a_tag.get("href")        
        if image_link != None: 
            link_text = a_tag.text.strip()  # Extract link text
            modified_link = f"{link_text}: {image_link}"  # Combine link text and image link
            a_tag.replace_with(modified_link)

    # Handle <img> tags
    for img_tag in soup.find_all("img"):
        image_link = img_tag["src"]
        alt_text = img_tag.get("alt", "")  # Extract alt text (default to empty string if not present)
        modified_link = f"{alt_text}: {image_link}"
        img_tag.replace_with(modified_link)

        # Extract text from custom [quote ] [/quote] tags using regular expressions
    text = soup.get_text()
    quote_pattern = r"\[quote\s+([^\]]*)\](.*?)\[\/quote\]"  # Match pattern with optional attributes
    matches = re.findall(quote_pattern, text, flags=re.DOTALL)  # Find all matches, including newlines
    for attributes, quote_text in matches:
        # Process attributes if needed (e.g., extract userid and url)
        text = text.replace(f"[quote {attributes}]", "\nQuote: ").replace("[/quote]", "\n")

    return text

def create_response_hierarchy(thread_and_reply):
    """
    Creates a nested dictionary representing thread hierarchies with reply bodies,
    from a list of reply dictionaries.

    Args:
        replies: A list of dictionaries, where each dictionary contains:
            - 'ReplyId': The unique ID of the reply.
            - 'ParentId': The ID of the parent reply, or None if it's a root thread.
            - 'Body': The text content of the reply.

    Returns:
        A nested dictionary where keys are thread IDs and values are lists of dictionaries.
        Each inner dictionary contains 'ReplyId', 'ParentId', and 'Body'.
    """

    threads = {}
    replies = thread_and_reply['Replies']
    original_Id = thread_and_reply['ThreadId']

    # Set the initial key to the JSON hierarchy
    threads[original_Id] = []

    for reply in replies:
        reply_id = reply['ReplyId']
        parent_id = reply.get('ParentId')
        body = reply.get('Body')  # Extract body, handling potential absence

        if parent_id is None:
            threads[original_Id] = {
                'ReplyId': reply_id,
                'Body': clean_body_text(body)
            }
        else:
            threads.setdefault(parent_id, {}).update({
                'ReplyId': reply_id,
                'Body': clean_body_text(body),
            })

    return threads

def process_dialogue(thread_and_reply): 
    """
        <>

        Args:
            thread_and_reply: A list of dictionaries, where each dictionary contains:
                - 'Body': The text content of the reply.

        Returns:
            A list with nested dictionaries where keys are:
                - role: defines user/chatbot
                - content: the main text for the dialogue thread
    """

    # now process the additional data
    response_hierarchy = create_response_hierarchy(thread_and_reply)

    # 0 = user, 1 = chatbot
    user_or_chatbot = 0
    role = "user"
    processed_dialogue = []

    # Add in the original thread body
    first_entry = {"role": role, "content": clean_body_text(thread_and_reply['Body'])}
    processed_dialogue.append(first_entry)

    # Access and process the nested structure with reply bodies:
    for id in response_hierarchy:
        # if no replies, return
        if len(response_hierarchy[id]) == 0:
            return []
        user_or_chatbot = not user_or_chatbot
        if user_or_chatbot == 0:
            role = "user"
        else:
            role = "assistant"
        assigned_reply = {"role": role, "content": response_hierarchy[id]['Body']}
        processed_dialogue.append(assigned_reply)
    
    return processed_dialogue
