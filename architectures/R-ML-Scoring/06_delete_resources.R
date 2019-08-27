
# 06_delete_resources.R

# This deletes all resources in the deployment resource group, as well as the
# service principal

# Run time ~2 minutes

# Clean up resources -----------------------------------------------------------

library(dotenv)

source("R/utilities.R")

# Delete the resource group

AzureRMR::get_azure_login(get_env("TENANT_ID"))$
  get_subscription(get_env("SUBSCRIPTION_ID"))$
  delete_resource_group(get_env("RESOURCE_GROUP"), confirm=FALSE)


# Delete the service principal

AzureGraph::get_graph_login(get_env("TENANT_ID"))$
  delete_app(get_env("SERVICE_PRINCIPAL_APPID"), confirm=FALSE)
