# Databricks notebook source
# MAGIC %pip install datasets

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from datasets import load_dataset

dataset_name = "mosaicml/dolly_hhrlhf"
dataset = load_dataset(dataset_name, split="train")

# COMMAND ----------

data

# COMMAND ----------

def apply_prompt_template(examples):
  instruction = examples["prompt"]
  response = examples["response"]

  return { "text": instruction +  response}

dataset = dataset.map(apply_prompt_template)
