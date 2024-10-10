# Databricks notebook source
df = spark.read.csv("/Volumes/llm_poc_catalog_westus2/landing/databrickslandingsa-llm-container/FAE_Feedback.csv",header=True)

# COMMAND ----------

print(df)

# COMMAND ----------

df.write.format("delta").mode("overwrite").option('overwriteSchema','true').save("/mnt/delta/Employee") 

# COMMAND ----------

spark.sql("CREATE TABLE employee USING DELTA LOCATION '/mnt/delta/Employee/'")
