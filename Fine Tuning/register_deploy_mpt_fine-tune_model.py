# Databricks notebook source
# MAGIC %md # Register your model into your workspace model registry and deploy the model
# MAGIC
# MAGIC This notebook shows an example how to register your model into your workspace registry instead of Unity catalog.
# MAGIC
# MAGIC Please notice by this way, your model will be stored in DBFS instead of your Azure storage connected to your catalog.  
# MAGIC
# MAGIC Cluster spec to run this notebook: i3.xlarge, 14.3 LTS ML
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Register the model to Databricks workspace model registry
# MAGIC  By default, MLflow registers models in the Databricks workspace model registry. 

# COMMAND ----------

import mlflow
registered_name = "mpt_30b_lora_fine_tune" # replace with your own model name 
run_id = "3834ff02f5a841e3a4c8336b7cfe02c7" # replace with your run_id that Log the fine tuned model to MLFlow 

result = mlflow.register_model(
    "runs:/"+run_id+"/model",
    registered_name,
)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Notice: "MlflowException: Exceeded max wait time" may appear, but it is OK. Please go to "models" in the left pannel and wait until you see your model version become ready, then execute the next cell for endpoint creation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Model Serving Endpoint
# MAGIC Once the model is registered, we can use API to create a Databricks GPU Model Serving Endpoint that serves the model.
# MAGIC

# COMMAND ----------

import requests
import json
databricks_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None) # recommend to use secrete 

deploy_headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
deploy_url = f'{databricks_url}/api/2.0/serving-endpoints'

# model_version = result  # the returned result of mlflow.register_model
endpoint_config = {
  "name": "mpt_30b_lora_fine_tune",
  "config": {
    "served_models": [{
      "name": "mpt_30b_lora_fine_tune-1", #f'{model_version.name.replace(".", "_")}_{model_version.version}',
      "model_name": "mpt_30b_lora_fine_tune", #model_version.name,
      "model_version": 1, #model_version.version,
      "workload_type": "GPU_LARGE",
      "workload_size": "Small",
      "scale_to_zero_enabled": "False"
    }]
  }
}
endpoint_json = json.dumps(endpoint_config, indent='  ')

# Send a POST request to the API
deploy_response = requests.request(method='POST', headers=deploy_headers, url=deploy_url, data=endpoint_json)

if deploy_response.status_code != 200:
  raise Exception(f'Request failed with status {deploy_response.status_code}, {deploy_response.text}')

# Show the response of the POST request
# When first creating the serving endpoint, it should show that the state 'ready' is 'NOT_READY'
# You can check the status on the Databricks model serving endpoint page, it is expected to take ~35 min for the serving endpoint to become ready
print(deploy_response.json())

# COMMAND ----------

# MAGIC %md ## Go to your endpoint page, wait until the endpoint is ready. 
