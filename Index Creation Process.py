# Databricks notebook source
# MAGIC %pip install -r requirements.txt

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

def main():
    if __name__ == '__main__':
       
            from pipelines.ingestion_pipeline.src.pdf_processing_pipeline.src.pdf_processing_pipeline import PDFProcessingPipeline
 
            process_pdf = PDFProcessingPipeline(database_index = "single_file_test_index")
 
            pdf_folder_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/test_folder_002/"
 
            process_pdf.run_pipeline(pdf_folder_path = pdf_folder_path)
 
main()

# COMMAND ----------


