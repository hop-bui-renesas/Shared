# Databricks notebook source
# MAGIC %pip install -r requirements.txt
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %pip install --force-reinstall pipelines-0.0.1-py2.py3-none-any.whl

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from pipelines.ingestion_pipeline.src.pdf_processing_pipeline.src.pdf_processing_pipeline import PDFProcessingPipeline

process_pdf = PDFProcessingPipeline(database_index = "test_large_file_index")

pdf_folder_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/test_folder_002"

process_pdf.run_pipeline(pdf_folder_path = pdf_folder_path) 

# Renesas_FAE_MVP/unit_tests/download_all_pdf/da14682-datasheet.pdf 460 page


# COMMAND ----------


