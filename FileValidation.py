# Databricks notebook source
from pyspark.sql.functions import col

# COMMAND ----------

import os
from pyspark.sql.functions import col

# Replace with your CSV file path
csv_file_path = "file:/Workspace/Shared/pdf_pages_data.csv"

# Replace with the target directory containing PDF files
pdf_file_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/all_product_family_pdf"

ble_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/productfamily_BLE"
ra_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/productfamily_RA"
misc_dir = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/productfamily_MISC"

df = spark.read.csv(csv_file_path, header=True)
# Filter file names from the CSV column (adjust the column name)
file_names_df = df.select(col("filename"))  # Replace "filename" with the actual column name

# Get all PDF file names
all_pdf_file_names = [f for f in os.listdir(pdf_file_dir) if f.endswith(".pdf")]
ble_pdf_file_names = [f for f in os.listdir(ble_dir) if f.endswith(".pdf")]
ra_pdf_file_names = [f for f in os.listdir(ra_dir) if f.endswith(".pdf")]
misc_pdf_file_names = [f for f in os.listdir(misc_dir) if f.endswith(".pdf")]

# COMMAND ----------

# Get all of these file names from file_names_df into a list
file_names_list = file_names_df.select("filename").rdd.flatMap(lambda x: x).collect()

# COMMAND ----------

len(file_names_list)

# COMMAND ----------

print("All PDF Files: ", len(all_pdf_file_names))
print("BLE PDF Files: ", len(ble_pdf_file_names))
print("RA PDF Files: ", len(ra_pdf_file_names))
print("MISC PDF Files: ", len(misc_pdf_file_names))

# COMMAND ----------

total = len(ble_pdf_file_names) + len(ra_pdf_file_names) + len(misc_pdf_file_names)
total

# COMMAND ----------

# Find non-existing file names
non_existing_files = list(set(file_names_list) - set(all_pdf_file_names))

# Print non-existing file names
print("Non-existing files:")
for i, filename in enumerate(non_existing_files):
    print(f"{i+1}. {filename}")

# COMMAND ----------

# MAGIC %pip install fitz
# MAGIC %pip install PyMuPDF
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import fitz

# Replace with your PDF file path
pdf_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/all_product_family_pdf/120-degree Conducting Control of Permanent Magnet Synchronous Motor with Hall Sensors.pdf"

# Open the PDF document
doc = fitz.open(pdf_path)

# Count the number of pages
num_pages = doc.page_count

# Print the number of pages
print(f"The PDF file has {num_pages} pages.")


# COMMAND ----------

type(doc)

# COMMAND ----------

# MAGIC %pip install tqdm
# MAGIC %pip install fitz
# MAGIC %pip install PyMuPDF
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from tqdm import tqdm
import os
import fitz
from concurrent.futures import ThreadPoolExecutor

# COMMAND ----------

def filter_documents(pdf_file, page_count_limit = 100):
    doc = fitz.open(pdf_file)
    total_page_count = doc.page_count
    if total_page_count <= page_count_limit:
        return pdf_file

pdf_folder_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/all_product_family_pdf"
pdf_files_list = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

print("Starting threaded filtering...")

# with ThreadPoolExecutor(max_workers=4) as filter_executor:
#     result = list(tqdm(filter_executor.map(filter_documents, pdf_files_list), total = len(pdf_files_list)))
with ThreadPoolExecutor(max_workers=4) as execut:
    ex = execut.map(filter_documents, pdf_files_list)
    
print("Threaded filtering complete...")

# COMMAND ----------

file_list = list(ex)

# COMMAND ----------

len(file_list)

# COMMAND ----------

print(result)
pdf_filtered_list = list(result)

# pdf_filtered_list = [filter_documents(i) for i in tqdm(pdf_files_list) if filter_documents(i) is not None]


print("Length of filtered list: ", len(pdf_filtered_list))
print("Filtered list: ", pdf_filtered_list)

