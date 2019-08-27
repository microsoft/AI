![](https://dev.azure.com/customai/AMLBatchScoringPipeline/_apis/build/status/Microsoft.AMLBatchScoringPipeline?branchName=master)

### Author: Said Bleik

# Deploying a Batch Scoring Pipeline for Python Models

## Overview
#### Scoring Anomaly Detection Models at Scale using Azure Machine Learning
In this repository you will find a set of scripts and commands that help you build a scalable solution for scoring many models in parallel using Azure Machine Learning (AML).

The solution can be used as a template and can generalize to different problems. The problem addressed here is monitoring the operation of a large number of devices in an IoT setting, where each device sends sensor readings continuously. We assume there are pre-trained [anomaly detection models](http://scikit-learn.org/stable/modules/outlier_detection.html#outlier-detection) - one for each sensor of a device. The models are used to predict whether a series of measurements, that are aggregated over a predefined time interval, correspond to an anomaly or not.

To get started, read through the *Design* section, then go through the following sections to create the Python environment, Azure resources, and the scoring pipeline:

* Design
* Prerequisites
* Create Environment
* Steps
    * Create Azure Resources
    * Create and Schedule the Scoring Pipeline
    * Validate Deployments and Pipeline Execution
* Cleanup

## Design
![System Architecture](./architecture.PNG)

This solution consists of several Azure cloud services that allow upscaling and downscaling resources according to need. The services and their role in this solution are described below.

### Blob Storage
Blob containers are used to store the pre-trained models, the data, and the output predictions. The models that we upload to blob storage in the [*01_create_resources.ipynb*](01_create_resources.ipynb) notebook are [One-class SVM](http://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html) models that are trained on data that represents values of different sensors of different devices. We assume that the data values are aggregated over a fixed interval of time. In real-world scenarios, this could be a stream of sensor readings that need to be filtered and aggregated before being used in training or real-time scoring. For simplicity, we use the same data file when executing scoring jobs.

### Azure Machine Learning
Azure Machine Learning (AML) is a cloud service that allows training, scoring, managing, and deploying machine learning models at scale in the cloud. It can be used to execute training, scoring, or other demanding jobs on remote compute targets, such as a cluster of virtual machines, that can scale according to need. In this solution guide, we use AML to run scoring jobs for many sensors in parallel. We do that by creating an AML pipeline with parallel steps, where each step executes a scoring Python [script](scripts/predict.py) for each sensor. AML manages queueing and executing the steps on a scalable compute target.

In addition, we create a scheduling process using AML to run the pipeline continuously on a specified time interval.


> For more information on these services, check the documentation links provided in the *Links* section. 

## Prerequisites
- [conda 4.5](https://conda.io/docs/user-guide/install/index.html)


> *All scripts and commands were tested on an Ubuntu 16.04 LTS system.*

## Create Environment
Once all prerequisites are installed,

1. Clone or download this repsitory:

    ```
    git clone https://github.com/Microsoft/AMLBatchScoringPipeline.git
    ```
2. Create and select conda environment from yml file:
        
    ``` 
    conda env create -f environment.yml
    conda activate amlmm    
    ```
3. Login to Azure and select subscription
    ```
    az login --use-device-code
    az account set -s "<subscription name or ID>"
    ```

4. Start Jupyter in the same environment:
    
    ```
    jupyter notebook
    ```
5. Open Jupyter Notebook in your browser and make sure your environemnt's kernel is selected: 

    ```
    Kernel > Change Kernel > Python [conda env:amlmm]
    ```

Start creating the required resources in the next section.

## Steps
### 1. Create Azure Resources
The [01_create_resources.ipynb](01_create_resources.ipynb) notebook contains all Azure CLI commands needed to create resources in your Azure subscription, as well as configurations of the AML pipeline and the compute target. 

Navigate to the cloned/downloaded directory in Jupyter Notebook: *AMLBatchScoringPipeline/01_create_resources.ipynb*, and start executing the cells to create the needed Azure resources. 

### 3. Create and Schedule the Scoring Pipeline
The [02_create_pipeline.ipynb](02_create_pipeline.ipynb) notebook contains Python code that creates the AML scoring pipeline and schedules it to run on a predefined interval.

### 2. Validate Deployments and Jobs Execution 
After all resources are created, you can check your resource group in the portal and validate that all components have been deployed successfully. 


Under *Storage Account > Blobs*, you should see the predictions' CSV files in the *preds* container, after the pipeline runs successfully.


## Cleaning up
If you wish to delete all created resources, run the following CLI command to delete the resource group and all underlying resources.

```sh
az group delete --name <resource_group_name>
```

## Links
- [End-to-End Anomaly Detection Jobs using Azure Batch AI](https://github.com/saidbleik/batchai_mm_ad)
- [Azure Machine Learning Documentation](https://docs.microsoft.com/en-us/azure/machine-learning/)
- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)

## Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
