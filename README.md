# Samples, Reference Architectures & Best Practices

This repository is meant to organize Microsoft's Open Source AI based repositories.

# Keywords
batch scoring, realtime scoring, model training, MLOps, Azure Machine Learning, computer vision, natural language processing, recommenders

## Table of contents
1. [Getting Started](#Getting-Started)
2. [AI100 - Samples](#ai100)
3. [AI200 - Reference Architectures](#ai200)
4. [AI300 - Best Practices](#ai300)
6. [Contributing](#Contributing)

# Getting Started <a name="Getting-Started"></a>
This repository is arranged as submodules so you can either pull all the tutorials or simply the ones you want. 
To pull all the tutorials run:

```bash
git clone --recurse-submodules https://github.com/microsoft/ai
```

if you have git older than 2.13 run:

```bash
git clone --recursive https://github.com/microsoft/ai.git
```

To pull a single submodule (e.g. DeployDeepModelKubernetes) run:
```
git clone https://github.com/microsoft/ai
cd ai
git submodule init submodules/DeployDeepModelKubernetes
git submodule update
```
# [AI100 - Samples](https://azure.microsoft.com/en-us/overview/ai-platform/)<a name="ai100"></a>
Samples are a collection of open source Python repositories created by the Microsoft product teams, which focus on AI services.  

| Title | Description | 
|-------|-------------|
| [Azure ML Python SDK](https://github.com/Azure/MachineLearningNotebooks)|Python notebooks with ML and deep learning examples with Azure Machine Learning|
| [Azure Cognitive Services Python SDK](https://github.com/Azure-Samples/cognitive-services-python-sdk-samples)|Learn how to use the Cognitive Services Python SDK with these samples |
| [Azure Intelligent Kiosk](https://github.com/microsoft/Cognitive-Samples-IntelligentKiosk)|Here you will find several demos showcasing workflows and experiences built on top of the Microsoft Cognitive Services.|
| [MML Spark Samples](https://github.com/Azure/mmlspark/tree/master/notebooks/samples)|MMLSpark is an ecosystem of tools aimed towards expanding the distributed computing framework Apache Spark in several new directions.|
| [Seismic Deep Learning Samples](https://github.com/microsoft/seismic-deeplearning/)|Deep Learning for Seismic Imaging and Interpretation.|

# [AI200 - Reference Architectures](https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/machine-learning-at-scale) <a name="ai200"></a>
Our reference architectures are arranged by scenario. Each architecture includes open source practices, along with considerations for scalability, availability, manageability, and security.

| Title                                     | Language | Environment | Design | Description                                                                       | Status                                                                                                                                                                                                                                                                                                              |
|----------------------------------------------|-------------|-------------|-------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Deploy Classic ML Model on Kubernetes](https://github.com/microsoft/MLAKSDeployAML)       						   | Python | CPU  | Real-Time Scoring| Train LightGBM model locally using Azure ML, deploy on Kubernetes or IoT Edge for _real-time_ scoring                         | [![Build Status](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_apis/build/status/AI%20CAT/Python-ML-RealTimeServing?branchName=master)](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_build/latest?definitionId=21&branchName=master)
| [Deploy Deep Learning Model on Kubernetes](https://github.com/microsoft/AKSDeploymentTutorialAML)    				   | Python | Keras | Real-Time Scoring| Deploy image classification model on Kubernetes or IoT Edge for _real-time_ scoring using Azure ML             | [![Build Status](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_apis/build/status/AI%20CAT/Python-Keras-RealTimeServing?branchName=master)](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_build/latest?definitionId=17&branchName=master)
| [Hyperparameter Tuning of Classical ML Models](https://github.com/Microsoft/MLHyperparameterTuning) 				   | Python | CPU  | Training | Train LightGBM model locally and run Hyperparameter tuning using Hyperdrive in Azure ML                            | ![](https://dev.azure.com/customai/MLHyperparameterTuningPipeline/_apis/build/status/Microsoft.MLHyperparameterTuning?branchName=master)                                                                                                                                                                            |
| [Deploy Deep Learning Model on Pipelines](https://github.com/Azure/Batch-Scoring-Deep-Learning-Models-With-AML)      | Python | GPU  | Batch Scoring | Deploy PyTorch style transfer model for _batch_ scoring using Azure ML Pipelines            | [![Build Status](https://dev.azure.com/customai/BatchScoringDeepLearningModelsWithAMLPipeline/_apis/build/status/Azure.Batch-Scoring-Deep-Learning-Models-With-AML?branchName=master)](https://dev.azure.com/customai/BatchScoringDeepLearningModelsWithAMLPipeline/_build/latest?definitionId=9&branchName=master) |
| [Deploy Classic ML Model on Pipelines](https://github.com/Microsoft/AMLBatchScoringPipeline)         				   | Python | CPU  | Batch Scoring | Deploy one-class SVM for _batch_ scoring anomaly detection using Azure ML Pipelines | ![](https://dev.azure.com/customai/AMLBatchScoringPipeline/_apis/build/status/Microsoft.AMLBatchScoringPipeline?branchName=master)                                                                                                                                                                                  |
| [Deploy R ML Model on Kubernetes](https://github.com/Azure/RealtimeRDeployment)         							   | R | CPU | Real-Time Scoring       | Deploy ML model for _real-time_ scoring on Kubernetes |  |
| [Deploy R ML Model on Batch](https://github.com/Azure/RBatchScoring)         										   | R | CPU  | Scoring     | Deploy forecasting model for _batch_ scoring using Azure Batch and doAzureParallel |  | 
| [Deploy Spark ML Model on Databricks](https://github.com/Azure/BatchSparkScoringPredictiveMaintenance)         	   | Python | Spark  | Batch Scoring | Deploy a classification model for _batch_ scoring using Databricks |                                                                                                                                                                                 |
| [Train Distributed Deep Leaning Model](https://github.com/Azure/DistributedDeepLearning/)         				   | Python | GPU  | Training | Distributed training of ResNet50 model using Batch AI |                                                                                                                                                                                  |

# AI300 - Best Practices <a name="ai300"></a>
Our best practices are arranged by topic. Each best pratice repository includes open source methods, along with considerations for scalability, availability, manageability, and security.

| Title | Description | 
|-------|-------------|
|[Computer Vision](https://github.com/microsoft/computervision)| Accelerate the development of computer vision applications with examples and best practice guidelines for building computer vision systems
|[Natural Language Processing](https://github.com/microsoft/nlp)|State-of-the-art methods and common scenarios that are popular among researchers and practitioners working on problems involving text and language.|
|[Recommenders](https://github.com/microsoft/recommenders)| Examples and best practices for building recommendation systems, provided as Jupyter notebooks.| 
|[MLOps](https://github.com/microsoft/MLOps)| MLOps empowers data scientists and app developers to help bring ML models to production. |


## Recommend a Scenario
If there is a particular scenario you are interested in seeing a tutorial for please fill in a [scenario suggestion](https://github.com/Microsoft/AIReferenceArchitectures/issues/new?assignees=&labels=&template=scenario_request.md&title=%5BSCENARIO%5D)

## Ongoing Work
We are constantly developing interesting AI reference architectures using Microsoft AI Platform. Some of the ongoing projects include IoT Edge scenarios, model scoring on mobile devices, add more... To follow the progress and any new reference architectures, please go to the AI section of this [link](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/).

# Contributing <a name="Contributing"></a>

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
