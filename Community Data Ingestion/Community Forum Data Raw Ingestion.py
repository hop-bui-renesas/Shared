# Databricks notebook source
# MAGIC %pip install --force-reinstall pipelines-0.0.1-py2.py3-none-any.whl
# MAGIC %pip install datasets
# MAGIC %pip install beautifulsoup4
# MAGIC %pip install lxml
# MAGIC %pip install langchain
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json
from datasets import load_dataset
from pipelines.cognitive_search_ingestion_pipeline.src.dialog_data_processing_pipeline.ForumIngestor import ForumIngestor

# COMMAND ----------


forum_info = {
    "Bluetooth Low Energy": "297",
    "RA MCU": "256"
}

save_file = "Forum_RAG_Format.json"
num_workers = 8

ingestor = ForumIngestor(forum_info=forum_info, save_file = save_file, format_type="rag")

file_path = ingestor.process_community_data()

# COMMAND ----------


