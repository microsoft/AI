
# 02_deploy_azure_resources.R
# 
# This script sets up Azure resources including the Batch cluster and the blob
# container where the data will be stored. The original dataset is replicated 
# from 11 SKUs of one product to 1000 SKUs of 90 products. The docker image to be 
# deployed on each cluster node is defined and pushed to your Docker Hub account.
#
# Note: you must have logged in to your Docker Hub account and the Azure CLI.
#
# Run time ~6 minutes


# Set environment variables ----------------------------------------------------

library(dotenv)
library(jsonlite)
library(doAzureParallel)
library(AzureStor)
library(AzureContainers)

source("R/options.R")
source("R/utilities.R")
source("R/create_cluster_json.R")
source("R/create_credentials_json.R")

set_resource_specs()

# Create resource group

az <- try(AzureRMR::get_azure_login(get_env("TENANT_ID")), silent=TRUE)
if(inherits(az, "try-error"))
  az <- AzureRMR::create_azure_login(get_env("TENANT_ID"), auth_type = "device_code")

sub <- az$get_subscription(get_env("SUBSCRIPTION_ID"))
rg <- sub$create_resource_group(get_env("RESOURCE_GROUP"),
  location=get_env("REGION"))


# Create service principal

gr <- try(AzureGraph::get_graph_login(get_env("TENANT_ID")), silent=TRUE)
if(inherits(gr, "try-error"))
  gr <- AzureGraph::create_graph_login(get_env("TENANT_ID"), auth_type="device_code")

app <- gr$create_app(get_env("SERVICE_PRINCIPAL_NAME"))

# retry until successful -- app takes time to appear
for(i in 1:20) {
  Sys.sleep(5)
  res <- try(rg$add_role_assignment(app, "Contributor"), silent=TRUE)
  if(!inherits(res, "try-error"))
    break
}
if(inherits(res, "try-error")) {
  stop("Unable to set access permissions for service principal")
}

set_env("SERVICE_PRINCIPAL_APPID", app$properties$appId)
set_env("SERVICE_PRINCIPAL_CRED", app$password)


# Create storage account and container

stor <- rg$create_storage_account(get_env("STORAGE_ACCOUNT_NAME"),
  kind="BlobStorage",
  wait=TRUE)

set_env("STORAGE_ACCOUNT_KEY", stor$list_keys()[1])

endp <- stor$get_blob_endpoint()
cont <- create_blob_container(endp, get_env("BLOB_CONTAINER_NAME"))

set_env("BLOB_CONTAINER_URL", paste0(cont$endpoint$url, cont$name, "/"))


# Create Azure container registry

acr <- rg$create_acr(get_env("ACR_NAME"))
registry <- acr$get_docker_registry()

set_env("REGISTRY_USERNAME", registry$username)
set_env("REGISTRY_PASSWORD", registry$password)
set_env("REGISTRY_URL", registry$server)

# Create batch account

rg$create_resource(type="Microsoft.Batch/batchAccounts",
  name=get_env("BATCH_ACCOUNT_NAME"),
  properties=list(
    AutoStorage=list(storageAccountId=stor$id)
  )
)


# Replicate data ---------------------------------------------------------------

# Expand data to 1000 SKUs from 90 products

lapply(2:floor(TARGET_SKUS / 11),
       function(m) {
         file.copy("data/history/product1.csv",
                   paste0("data/history/product", m, ".csv"),
                   overwrite = TRUE)
         file.copy("data/futurex/product1.csv",
                   paste0("data/futurex/product", m, ".csv"),
                   overwrite = TRUE)
       })


# upload resources -------------------------------------------------------------

multiupload_blob(cont, src = "data/history/*", dest = "data/history")
multiupload_blob(cont, src = "data/futurex/*", dest = "data/futurex")
multiupload_blob(cont, src = "models/*", dest = "models")


# Build worker docker image ----------------------------------------------------

# The worker docker container will be deployed on each node of the Batch cluster.
# The dockerfile used to build to the worker docker image can be reviewed in
# docker/worker/dockerfile


# Build and upload the worker docker image to Docker Hub

worker <- get_env("WORKER_CONTAINER_IMAGE")

call_docker(sprintf("build -t %s -f docker/worker/dockerfile .", worker))
registry$push(worker)


# Define cluster ---------------------------------------------------------------

# Create json file to store doAzureParallel credentials

create_credentials_json()


# Set doAzureParallel credentials

doAzureParallel::setCredentials("azure/credentials.json")


# Create the cluster config file and provision the cluster

create_cluster_json <- function(save_dir = "azure") {
  
  config <- list(
    name = get_env("CLUSTER_NAME"),
    vmSize = get_env("VM_SIZE"),
    maxTasksPerNode = 1,
    poolSize = list(
      dedicatedNodes = list(
        min = 0,
        max = as.integer(get_env("NUM_NODES"))
      ),
      lowPriorityNodes = list(
        min = 0,
        max = 0
      ),
      autoscaleFormula = "QUEUE_AND_RUNNING"
    ),
    containerImage = paste0(get_env("ACR_NAME"), ".azurecr.io/", get_env("WORKER_CONTAINER_IMAGE")),
    commandLine = c()
  )
  
  config_json <- toJSON(config, auto_unbox = TRUE, pretty = TRUE)
  
  write(config_json, file = file.path(save_dir, "cluster.json"))
  
}

write_function(create_cluster_json, "R/create_cluster_json.R")

create_cluster_json(save_dir = "azure")

makeCluster("azure/cluster.json")
