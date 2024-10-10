# Databricks notebook source
# MAGIC %pip install pipelines-0.0.1-py2.py3-none-any.whl
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json
from datasets import load_dataset

# COMMAND ----------

from pipelines.ingestion_pipeline.src.dialog_data_processing_pipeline.ForumIngestor import ForumIngestor

forum_info = {
    "Bluetooth Low Energy": "297",
    "RA MCU": "256"
}

ingestor = ForumIngestor(forum_info=forum_info)

file_path = ingestor.process_community_data()

# COMMAND ----------

# Read in the pre-processed community forum JSON file
# TO BE REMOVED:
file_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/CommunityData/Forum_Fine_Tuning_Dialogue.json"

community_data = json.load(open(file_path))

# Insert a system message for training
sys_obj = {"role": 'system', 'content': 'You are a helpful, technical assistant that can engage in conversations about technical product specificaitons and how to use them in a various array of applications.'}
for thread in community_data['messages']:
    thread.insert(0, sys_obj)

# Assuming your DataFrame has a column named 'json_data'
jsonl_filename = '/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/CommunityData/finetune_data.jsonl'

# Convert threads to JSONL format
with open(jsonl_filename, 'w') as jsonl_file:
    for thread in community_data['messages']:
        for turn in thread: 
            turn['content'].encode("utf-8").decode("utf-8")
        new_object = {"messages": thread} 
        json_line = json.dumps(new_object)
        jsonl_file.write(json_line + '\n')

print(f"DataFrame converted to JSONL format and saved to {jsonl_filename}")

# COMMAND ----------

jsonl_filename = '/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/CommunityData/finetune_data.jsonl'

dataset = load_dataset("json", data_files=jsonl_filename, split="train")

# COMMAND ----------

len(dataset['messages'])

# COMMAND ----------

ds_dict = dataset.train_test_split(test_size=.20)

# COMMAND ----------

train_dataset = ds_dict['train']
test_dataset = ds_dict['test']

# COMMAND ----------

print(train_dataset)
print(test_dataset)

# COMMAND ----------

train_dataset['messages'][0][0]

# COMMAND ----------

#KB TEST

import os
from pipelines.ingestion_pipeline.src.qapair_processing_pipeline.finetune_processor import FineTunePrep

directory = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/processed_data/knowledge_base_faq/"

ft = FineTunePrep()

for filename in os.listdir(directory):
  if filename.endswith(".jsonl"):
    filepath = os.path.join(directory, filename)
    ft.files.append(filename)

    ft.create_finetune_dataset(filepath)

dataset = ft.full_dataset

# COMMAND ----------

dataset

# COMMAND ----------

def _reformat_data(rec):
    instruction = rec["instruction"]
    response = rec["response"]
    context = rec.get("context")

    if context:
    questions = PROMPT_WITH_INPUT_FORMAT.format(instruction=instruction, input=context)
    else:
    questions = PROMPT_NO_INPUT_FORMAT.format(instruction=instruction)
    return {"text": f"{{ 'prompt': {questions}, 'response': {response} }}"}

dataset = dataset.map(_reformat_data)

# COMMAND ----------

dataset

# COMMAND ----------

dataset['answer'][8]

# COMMAND ----------


