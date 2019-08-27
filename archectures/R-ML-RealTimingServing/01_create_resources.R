library(AzureGraph)
library(AzureRMR)
library(AzureContainers)

# create resource group and resources ---

source("resource_specs.R")

# create ARM and Graph logins
az <- try(get_azure_login(tenant), silent=TRUE)
if(inherits(az, "try-error"))
    az <- create_azure_login(tenant, auth_type="device_code")

gr <- try(get_graph_login(tenant), silent=TRUE)
if(inherits(gr, "try-error"))
    gr <- create_graph_login(tenant, auth_type="device_code")

sub <- az$get_subscription(sub_id)

deployresgrp <- (if(sub$resource_group_exists(rg_name))
    sub$get_resource_group(rg_name)
else sub$create_resource_group(rg_name, location=rg_loc))

deployresgrp$create_acr(acr_name)

# this will take several minutes (usually 10-20)
deployresgrp$create_aks(aks_name,
    agent_pools=aks_pools("agentpool", num_nodes))


