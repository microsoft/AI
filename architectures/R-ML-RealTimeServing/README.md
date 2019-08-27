### Author: Hong Ooi

# Real-time model deployment with R using Azure Container Registry and Azure Kubernetes Service

## Overview

This repository hosts deployment artifacts for the reference architecture "Real-time model deployment with R". You can use these artifacts to deploy a containerised predictive service in Azure.

## Design

![](https://github.com/mspnp/architecture-center/blob/master/docs/reference-architectures/ai/_images/realtime-scoring-r.png)

The workflow in this repository builds a sample machine learning model: a random forest for housing prices, using the Boston housing dataset that ships with R. It then builds a Docker image with the components to host a predictive service:
- Microsoft Machine Learning Server (only the R components).
- The Azure CLI (necessary to use Model Operationalization).
- the model object plus any packages necessary to use it (randomForest in this case).
- a script that is run on container startup.

This image is pushed to a Docker registry hosted in Azure, and then deployed to a Kubernetes cluster, also in Azure.

## Prerequisites

To use this repository, you should have the following:

- A recent version of R. It's recommended to use [Microsoft R Open](https://mran.microsoft.com/open), although the standard R distribution from CRAN will work perfectly well.

- The following packages for working with Azure. Note that if you are using Microsoft R, they will probably not be in the MRAN snapshot that is your default repository; run `options(repos="https://cloud.r-project.org")` to set your repository to an up-to-date CRAN mirror. before running `install.packages`.
  * [AzureRMR](https://cran.r-project.org/package=AzureRMR), a package that implements an interface to Azure Resource Manager
  * [AzureGraph](https://cran.r-project.org/package=AzureGraph), an interface to Microsoft Graph
  * [AzureContainers](https://cran.r-project.org/package=AzureContainers), an interface to ACR and AKS

- [Docker](https://www.docker.com/get-started), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [helm](https://www.helm.sh/) installed on your machine.

- An Azure subscription.


## Setup

Edit the file [`resource_specs.R`](resource_specs.R) to contain the following:

- Your Azure Active Directory tenant. This can be either your directory name or a GUID.
- Your subscription ID.
- The name of the resource group that will hold the resources created. The resource group will be created if it does not already exist.
- The location of the resource group; for a list of regions where AKS is available, see [this page](https://docs.microsoft.com/en-us/azure/aks/container-service-quotas#region-availability).
- The names for the ACR and AKS resources to be created.
- The number of nodes for the AKS cluster.

## Deployment steps

In general, you should _not_ run these scripts in an automated fashion, eg via `source()` or by pressing <kbd>Ctrl-Shift-Enter</kbd> in RStudio. This is because the process of creating and deploying resources in the cloud involves significant latencies; it's sometimes necessary to wait until a given step has finished before starting on the next step. Because of this, you should step through the scripts line by line, following any instructions in the comments.

### Building the model image

The script [`00_build_image.R`](00_build_image.R) trains a simple model (a random forest for house prices, using the Boston dataset), and then builds the Docker image for the predictive service. The image is about 2GB in size.

The MMLS install used in this image is licensed for development and testing purposes only. For a production image, contact your Microsoft representative about licensing details.

### Creating the Azure resources

The script [`01_create_resources.R`](01_create_resources.R) checks if the resource group for the deployment exists, and creates it if necessary. It then creates the ACR and AKS resources. Note that creating an AKS resource can take several minutes.

### Installing an ingress controller

The script [`02_install_ingress.R`](02_install_ingress.R) installs nginx on the Kubernetes cluster, and downloads a TLS certificate from Let's Encrypt.

### Deploying the service

The script [`03_deploy_service.R`](03_deploy_service.R) deploys the actual predictive service. First, it pushes the image built previously to the container registry, and then creates a deployment and service on the Kubernetes cluster using that image. This step involves uploading the image to Azure, so may take some time depending on the speed of your Internet connection. At the end, it brings up the Kubernetes dashboard so you can verify that the deployment has succeeded.

## Testing the service

The script [`04_test_service.R`](04_test_service.R) tests that the service works properly (which is not the same as testing that the deployment succeeded). It uses the httr package to send requests to the API endpoint; you can check that the responses are as expected.



