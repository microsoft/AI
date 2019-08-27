library(AzureRMR)
library(AzureContainers)

# resource/service objects ---
source("resource_specs.R")

sub <- get_azure_login(tenant)$
    get_subscription(sub_id)

deployresgrp <- sub$get_resource_group(rg_name)
deployclus_svc <- deployresgrp$get_aks(aks_name)

deployclus <- deployclus_svc$get_cluster()


### install ingress controller and enable https

# install nginx ---
deployclus$helm("init")

# may take several seconds for a tiller pod to become available: run this until the installation succeeds
deployclus$helm("install stable/nginx-ingress --namespace kube-system --set controller.replicaCount=2 --set rbac.create=false")


# install TLS certificate and ingress ---

# check that the ingress controller is up, and an external IP address has been assigned
# this can again take several seconds
deployclus$get("service", "--all-namespaces")

# get the IP address resource
# run this after an external IP has been assigned to the ingress controller
cluster_resources <- sub$
    get_resource_group(deployclus_svc$properties$nodeResourceGroup)$
    list_resources()

ip_res <- cluster_resources[[grep("IPAddresses", names(cluster_resources))]]
ip_res$sync_fields()

# assign domain name to IP address of cluster endpoint
ip_res$do_operation(
    body=list(
        location=ip_res$location,
        properties=list(
            dnsSettings=list(domainNameLabel="mls-model"),
            publicIPAllocationMethod=ip_res$properties$publicIPAllocationMethod)),
    encode="json",
    http_verb="PUT")

inst_certmgr <- gsub("\n", " ", "install stable/cert-manager
--namespace kube-system
--set ingressShim.defaultIssuerName=letsencrypt-staging
--set ingressShim.defaultIssuerKind=ClusterIssuer
--set rbac.create=false
--set serviceAccount.create=false")

deployclus$helm(inst_certmgr)

# deploy certificate and ingress controller
deployclus$apply(gsub("resgrouplocation", rg_loc, readLines("yaml/cluster-issuer.yaml")))
deployclus$apply(gsub("resgrouplocation", rg_loc, readLines("yaml/certificates.yaml")))
deployclus$apply(gsub("resgrouplocation", rg_loc, readLines("yaml/ingress.yaml")))
