### Authors: Yan Zhang
### Acknowledgements: Mathew Salvaris

# Deploying Python models on Azure IoT Edge

In this tutorial, we introduce how to deploy an ML/DL (machine learning/deep learning) module through [Azure IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/how-iot-edge-works). 

Azure IoT Edge is an Internet of Things (IoT) service that builds on top of Azure IoT Hub. It is a hybrid solution combining the benefits of the two scenarios: *IoT in the Cloud* and *IoT on the Edge*. This service is meant for customers who want to analyze data on devices, a.k.a. "at the edge", instead of in the cloud. By moving parts of your workload to the edge, your devices can spend less time sending messages to the cloud and react more quickly to changes in status. On the other hand, Azure IoT Hub provides centralized way to manage Azure IoT Edge devices, and make it easy to train ML models in the Cloud and deploy the trained models on the Edge devices.  

In this example, we how to deploy a Frequently Asked Questions (FAQ) matching model on Azure IoT Edge to provide predictions for user questions. For this scenario, “Input Data” in the architecture diagram refers to text strings containing the user questions to match with a list of FAQs. The model deployment process can be generalized to any scenario that uses Python models to make real-time predictions. When the image data is generated from a process pipeline and fed into the edge device, the deployed model can make predictions right on the edge device without accessing to the cloud. Following diagram shows the major components of an Azure IoT edge device. Source code and full documentation are linked below.

<p align="center">
<img src="azureiotedgeruntime.png" alt="logo" width="90%"/>
</p>

We perform following steps for the deployment.

- Step 1: Build the trained ML/DL model into docker image. This image will be used to create a docker container running on the edge device. 
- Step 2: Provision and Configure IoT Edge Device
- Step 3: Deploy ML/DL Module on IoT Edge Device
- Step 4: Test ML/DL Module


To get started with the tutorial, please proceed with following steps **in sequential order**.

 * [Prerequisites](#prerequisites)
 * [Steps](#steps)
 * [Cleaning up](#cleanup)
 

<a id='prerequisites'></a>
## Prerequisites
1. Linux (Ubuntu).
2. [Anaconda Python](https://www.anaconda.com/download)
3. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
4. [Azure account](https://azure.microsoft.com).

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

<a id='steps'></a>
## Steps
To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Docker and Azure seamlessly.

1. Add your user to the docker group:
    ```
    sudo usermod -aG docker $USER
    newgrp docker
   ```   
2. Login to Docker with your username and password:
    ```
    docker login
   ```
3. Create the Python MLAKSDeployAML virtual environment using the environment.yml:
   ```
   conda env create -f environment.yml
   ```
4. Activate the virtual environment:
   ```
   source activate MLAKSDeployAML
   ```
5. Login to Azure:
   ```
   az login
   ```
6. If you have more than one Azure subscription, select it:
   ```
   az account set --subscription <Your Azure Subscription>
   ```
7. Start the Jupyter notebook server in the virtual environment:
   ```
   jupyter notebook
   ```
8. After following the setup instructions above, run the Jupyter notebooks in order starting with the first notebook.

<a id='cleanup'></a>
## Cleaning up
To remove the conda environment created see [here](https://conda.io/docs/commands/env/conda-env-remove.html). The last Jupyter notebook also gives details on deleting Azure resources associated with this repository.

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
