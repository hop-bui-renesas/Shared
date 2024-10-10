# Databricks notebook source
# MAGIC %pip install -r requirements.txt

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

def main():
    # 
    from pipelines.ingestion_pipeline.src.pdf_processing_pipeline.src.pdf_processing_pipeline import PDFProcessingPipeline

    process_pdf = PDFProcessingPipeline(database_index = "gpu_multicore_100pages_90_pct_pdfs_v2")

    pdf_folder_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/all_product_family_pdf/"

    process_pdf.run_pipeline(pdf_folder_path = pdf_folder_path)
    
if __name__ == '__main__':
    main()

# COMMAND ----------


