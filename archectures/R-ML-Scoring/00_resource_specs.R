# Provide specifications for your deployment.

# Note: You must specify values for the variables under Account details. For all
# other names/values, defaults have been provided. The prefix "rbs" has been used
# for resource names (for "R Batch Scoring"). 

# The default cluster size is 10 nodes of size Standard_DS2_v2 which provides 
# good performance for this workload. The deployment can be scaled up or down by
# adding or subtracting nodes. For the workload in this scenario, increasing the
# size of each node will not improve performance significantly.


# Account details --------------------------------------------------------------

# Your Azure subscription ID

SUBSCRIPTION_ID <- ""


# The Tenant (Directory) ID of your Azure account on the Azure Active Directory.
# You can find this in the Azure Portal by navigating to All services > Azure
# Active Directory > Properties. Copy the Directory ID below.

TENANT_ID <- ""


# Deployment details -----------------------------------------------------------

# Azure region to deploy resources

REGION <- "southcentralus"


# Name of the resource group in which to deploy resources

RESOURCE_GROUP <- "rbsrg"


# The name of the service principal which will create resources in your
# subscription on your behalf

SERVICE_PRINCIPAL_NAME <- "rbsapp"

# Name of the Azure Batch Account

BATCH_ACCOUNT_NAME <- "rbsba"


# Name of the storage account to store data and logs

STORAGE_ACCOUNT_NAME <- "rbssa"


# Name of the blob container in which to store data and models

BLOB_CONTAINER_NAME <- "rbsbc"


# Name of the Azure Logic App to deploy

LOGIC_APP_NAME <- "rbsla"


# Name of the Azure Container Registry to deploy

ACR_NAME <- "rbsacr"

# Name of the Azure Container Instance to deploy

ACI_NAME <- "rbsaci"


# Cluster details --------------------------------------------------------------


# Name of the Azure Batch Cluster

CLUSTER_NAME <- "rbscl"


# Number of virtual machines in the cluster

NUM_NODES <- "10"


# Size of each VM

VM_SIZE <- "Standard_DS2_v2"


# Container details ------------------------------------------------------------

WORKER_CONTAINER_IMAGE <- "rbsworker"

SCHEDULER_CONTAINER_IMAGE <- "rbsscheduler"
