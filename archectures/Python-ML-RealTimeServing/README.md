![](https://dev.azure.com/customai/MLAKSDeployAMLPipeline/_apis/build/status/Microsoft.MLAKSDeployAML%20(master)?branchName=master)

### Authors: Fidan Boylu Uz, Yan Zhang
### Acknowledgements: Mario Bourgoin, Mathew Salvaris

# Deploying Python models for real-time scoring using Azure Machine Learning

In this repository there are a number of tutorials in Jupyter notebooks that have step-by-step instructions on (1) how to train a machine learning model using Python; (2) how to deploy a trained machine learning model throught Azure Machine Learning (AzureML). The tutorials cover how to deploy models on following deployment target:

- [Azure Kubernetes Service (AKS) Cluster](./{{cookiecutter.project_name}}/aks)
- [Azure IoT Edge](./{{cookiecutter.project_name}}/iotedge)

## Overview
This scenario shows how to deploy a Frequently Asked Questions (FAQ) matching model as a web service to provide predictions for user questions. For this scenario, “Input Data” in the [architecture diagram](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/realtime-scoring-python) refers to text strings containing the user questions to match with a list of FAQs. The scenario is designed for the Scikit-Learn machine learning library for Python but can be generalized to any scenario that uses Python models to make real-time predictions.

## Design
<!-- ![alt text](Design.png "Design") -->
The scenario uses a subset of Stack Overflow question data which includes original questions tagged as JavaScript, their duplicate questions, and their answers. It trains a Scikit-Learn pipeline to predict the match probability of a duplicate question with each of the original questions. These predictions are made in real time using a REST API endpoint.
The application flow for this architecture is as follows:
1.	The client sends a HTTP POST request with the encoded question data.
2.	The  webservice extracts the question from the request
3.	The question is then sent to the Scikit-learn pipeline model for featurization and scoring. 
4.	The matching FAQ questions with their scores are then piped into a JSON object and returned to the client.

An example app that consumes the results is included with the scenario.

## Prerequisites
1. Linux (Ubuntu).
2. [Anaconda Python](https://www.anaconda.com/download)
3. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
4. [Azure account](https://azure.microsoft.com).

---
**NOTE**
You will need to be able to run docker commands without sudo to run this tutorial. Use the following commands to do this.

```bash
sudo usermod -aG docker $USER
newgrp docker
``` 
---

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

## Setup
To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Docker and Azure seamlessly.
1. Create an _Ubuntu_ _Linux_ DSVM and perform the following steps.

2. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html), a tool creates projects from project templates.
```bash
pip install cookiecutter
```

3. Use cookiecutter to clone this repository. Cookiecutter will prompt a series of questions where you will choose a specific framework, select your deployment settings, and obtain an Azure ML workspace.
   ```bash
   cookiecutter https://github.com/Microsoft/MLAKSDeployAML.git
   ```
   You will be asked to choose or enter information such as *project name*, *subsciption id*, *resource group*, etc. in an interactive way. You can press *Enter* to accept the default value or enter a value of your choice. For example, if you want to learn how to deploy machine learing model on AKS Cluster, you should choose the value "aks" for variable *deployment_type*. Instead, if you want to learn about deploying machine learning model on IoT Edge, you should select "iotedge" for the variable *deployment_type*. 

   Provide a valid value for "subscription_id", otherwise a `subscription id is missing` error will be generated **after** all the questions are asked. You will have to perform Step 3 all over again. The full list of questions can be found in [cookiecutter.json](./cookiecutter.json) file. 

   Please make sure all entered information are correct, as these information are used to customize the content of your repo. 

4. On your local machine, you should now have a repo with the *project_name* you specified. Find the README.md file in this repo and proceed with instructions specified in it. 



# Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
