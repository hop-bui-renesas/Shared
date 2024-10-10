# Databricks notebook source
import os
from pyspark.sql.functions import col

# COMMAND ----------


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

# MAGIC %pip install tqdm
# MAGIC %pip install fitz
# MAGIC %pip install PyMuPDF
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import fitz
import os 

# Replace with your PDF file path
pdf_folder_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/pdf_files/all_product_family_pdf"

pdf_files_list = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

# COMMAND ----------

import tqdm

# COMMAND ----------

less_than_100 = 0
for i, path in enumerate(pdf_files_list):
    # Open the PDF document
    doc = fitz.open(path)
    # Count the number of pages
    num_pages = doc.page_count
    if num_pages <= 100:
        less_than_100+=1

print("File less than 100: ", less_than_100)

# COMMAND ----------



# COMMAND ----------

def split_pages(pdf_file, total_page_count, doc, chunk_page_size = 10):
    start = 0
    print("Entered Split Pages...")
    splitted_file = os.path.split(pdf_file)
    print("Split File: ", splitted_file)
    filename  = splitted_file[1].split(".")[0]
    print("File Name: ", filename)
    # filename = "pdf_file"

    if not os.path.exists(os.path.join(splitted_file[0],filename)):
        os.mkdir(os.path.join(splitted_file[0], filename))
    
    save_to = os.path.join(splitted_file[0], filename)

    splitted_pages = []
    page_chunk_count_list = []

    page_chunk_count = 0
    
    while start < total_page_count:
        with fitz.open() as doc_tmp:
            end = start + chunk_page_size - 1
            if end >= total_page_count:
                end = total_page_count
            doc_tmp.insert_pdf(doc, from_page=start, to_page=end, rotate=-1, show_progress=False)

            file_name = f"pdf_file_page_{start}_{end}.pdf"
            file_name = os.path.join(save_to, file_name)
            doc_tmp.save(file_name)
            start = end + 1
            splitted_pages.append(file_name)
            page_chunk_count_list.append(page_chunk_count)
            page_chunk_count = page_chunk_count + 1
    print("Completed Splitting the PDF Pages")
    return splitted_pages, page_chunk_count_list

# COMMAND ----------

file_path = "/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/test_folder_002/um-b-090-da1469x-getting-started-user-manual.pdf"
doc = fitz.open(file_path)
page_count = doc.page_count

# COMMAND ----------

split_pages, page_chunk_count_list = split_pages(file_path, page_count, doc)

# COMMAND ----------

for idx, split_pdf in enumerate(split_pages):
    print(f"file {idx}: {split_pdf}")
    # form recognizer for each file in the list

# COMMAND ----------

page_chunk_count_list

# COMMAND ----------


