
# 05_deploy_logic_app.R

# This script deploys a Logic App from an Azure Resource Manager (ARM)
# template. The Logic App will create an Azure Container Instance on a schedule
# set to run once a week. The ACI runs the 03_forecast_on_batch.R script to 
# generate forecasts.

# Note: after deploying the ARM template, you must authorize the ACI connector
# in the Azure Portal which gives permission to the Logic App to deploy the ACI.
# See the README.md file for instructions on how to do this.
#
# Run time ~6 minutes on a 5 node cluster


# Deploy Logic App -------------------------------------------------------------

library(dotenv)
library(jsonlite)
library(AzureRMR)
source("R/utilities.R")


# Insert resource names and environment variables into json template

file_name <- "azure/logic_app_template.json"
logic_app_json <- readLines(file_name)
logic_app_json <- replace_template_vars(logic_app_json)
writeLines(logic_app_json, "azure/logic_app.json")


# Deploy the Logic App

AzureRMR::get_azure_login(get_env("TENANT_ID"))$
  get_subscription(get_env("SUBSCRIPTION_ID"))$
  get_resource_group(get_env("RESOURCE_GROUP"))$
  deploy_template(get_env("LOGIC_APP_NAME"), "azure/logic_app.json", wait=TRUE)


# Now see README.md for instructions on how to complete the deployment, including
# authentication of the Logic App ACI connector and enabling the Logic App.
