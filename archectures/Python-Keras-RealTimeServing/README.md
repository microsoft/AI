### Authors: Yan Zhang, Mathew Salvaris, and Fidan Boylu Uz
[![Build Status](https://dev.azure.com/customai/AKSDeploymentTutorialAML/_apis/build/status/Microsoft.AKSDeploymentTutorialAML?branchName=master)](https://dev.azure.com/customai/AKSDeploymentTutorialAML/_build/latest?definitionId=11&branchName=master)
# Deploy Deep Learning CNN using Azure Machine Learning
## Overview
In this repository there are a number of tutorials in Jupyter notebooks that have step-by-step instructions on how to deploy a pretrained deep learning model on a GPU enabled Kubernetes cluster throught Azure Machine Learning (AzureML). The tutorials cover how to deploy models from the following deep learning frameworks on specific deployment target:
 
* Keras (TensorFlow backend)
  - [Azure Kubernetes Service (AKS) Cluster with GPUs](./{{cookiecutter.project_name}}/Keras_Tensorflow/aks)
  - [Azure IoT Edge](./{{cookiecutter.project_name}}/Keras_Tensorflow/iotedge)
* [Pytorch](./{{cookiecutter.project_name}}/Pytorch) (coming soon)

![alt text](https://happypathspublic.blob.core.windows.net/aksdeploymenttutorialaml/example.png "Example Classification")
 
 For each framework, we go through the following steps:
 * Create an AzureML Workspace
 * Model development where we load the pretrained model and test it by using it to score images
 * Develop the API that will call our model 
 * Building the Docker Image with our REST API and model and testing the image
 * AKS option
     * Creating our Kubernetes cluster and deploying our application to it
     * Testing the deployed model
     * Testing the throughput of our model
     * Cleaning up resources
 * IOT Edge option
     * Creating IoT hub and IoT Edge device identity, configuring the physical IOT Edge device, and deploying our application to it
     * Cleaning up resources
 
## Design

As described on the associated [Azure Reference Architecture page](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/realtime-scoring-python), the application we will develop is a simple image classification service, where we will submit an image and get back what class the image belongs to. The application flow for the deep learning model is as follows:
1)	Deep learning model is registered to AzureML model registry.
2)	AzureML creates a docker image including the model and scoring script.
3)	AzureML deploys the scoring image on the chosen deployment compute target (AKS or IoT Edge) as a web service.
4)	The client sends a HTTP POST request with the encoded image data.
5)	The web service created by AzureML preprocesses the image data and sends it to the model for scoring.
6)	The predicted categories with their scores are then returned to the client.


**NOTE**: The tutorial goes through step by step how to deploy a deep learning model on Azure; it **does** **not** include enterprise best practices such as securing the endpoints and setting up remote logging etc. 

**Deploying with GPUS:** For a detailed comparison of the deployments of various deep learning models, see the blog post [here](https://azure.microsoft.com/en-us/blog/gpus-vs-cpus-for-deployment-of-deep-learning-models/) which provides evidence that, at least in the scenarios tested, GPUs provide better throughput and stability at a lower cost.



# Getting Started

To get started with the tutorial, please proceed with following steps **in sequential order**.

 * [Prerequisites](#prerequisites)
 * [Setup](#setup)


<a id='prerequisites'></a>
## Prerequisites
1. Linux (x64) with GPU enabled.
2. [Anaconda Python](https://www.anaconda.com/download)
3. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
4. [Azure account](https://azure.microsoft.com).

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

<a id='setup'></a>
## Setup
To set up your environment to run these notebooks, please follow these steps.  
1. Create a _Linux_ Ubuntu DSVM (NC6 or above to use GPU).

2. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html), a tool creates projects from project templates.
```bash
pip install cookiecutter
```

3. Clone and choose a specific framework and deployment option for this repository. You will obtain a repository tailored to your choice of framework and deployment compute target.
   ```bash
   cookiecutter https://github.com/Microsoft/AKSDeploymentTutorialAML.git 
   ```
You will be asked to choose or enter information such as *framework*, *project name*, *subsciption id*, *resource group*, etc. in an interactive way. If a dafault value is provided, you can press *Enter* to accept the default value and continue or enter value of your choice. For example, if you want to learn how to deploy deep learning model on AKS Cluster using Keras, you should have values "keras" as the value for variable *framework* and "aks" for variable *deployment_type*. Instead, if you want to learn deploying deep learning model on IoT Edge, you should select "iotedge" for variable *deployment_type*. 

You must provide a value for "subscription_id", otherwise the project will fail with the error "ERROR: The subscription id is missing, please enter a valid subscription id" after all the questions are asked. The full list of questions can be found in [cookiecutter.json](./cookiecutter.json) file. 

Please make sure all entered information are correct, as these information are used to customize the content of your repo. 


4. With the generation of the project custom readmes will be created based on  [aks-keras](./{{cookiecutter.project_name}}/Keras_Tensorflow/aks/README.md) or [iotedge-keras](./{{cookiecutter.project_name}}/Keras_Tensorflow/iotedge/README.md). Go find a README.md file in your project directory and proceed with instructions specified in it. 



# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

