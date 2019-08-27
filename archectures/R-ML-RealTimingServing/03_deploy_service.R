library(AzureRMR)
library(AzureContainers)

# resource/service objects
source("resource_specs.R")

deployresgrp <- get_azure_login(tenant)$
    get_subscription(sub_id)$
    get_resource_group(rg_name)


### deploy predictive model as a service

# push image to registry
deployreg_svc <- deployresgrp$get_acr(acr_name)
deployreg <- deployreg_svc$get_docker_registry()

deployreg$push("mls-model")


# create the deployment and service ---

deployclus_svc <- deployresgrp$get_aks(aks_name)

# give AKS pull access to ACR
aks_app_id <- deployclus_svc$properties$servicePrincipalProfile$clientId
deployreg_svc$add_role_assignment(
    principal=AzureGraph::get_graph_login(tenant)$get_app(aks_app_id),
    role="Acrpull"
)

deployclus <- deployclus_svc$get_cluster()

deployclus$create(gsub("registryname", acr_name, readLines("yaml/deployment.yaml")))
deployclus$create("yaml/service.yaml")


# check on deployment/service status: can take a few minutes
deployclus$get("deployment")
deployclus$get("service")

# display the dashboard
deployclus$show_dashboard()
