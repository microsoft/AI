[![Build Status](https://dev.azure.com/customai/BatchScoringDeepLearningModelsWithAMLPipeline/_apis/build/status/Azure.Batch-Scoring-Deep-Learning-Models-With-AML?branchName=master)](https://dev.azure.com/customai/BatchScoringDeepLearningModelsWithAMLPipeline/_build/latest?definitionId=9&branchName=master)

# Batch Scoring Deep Learning Models With Azure Machine Learning

## Overview
As described in the associated page on the [Azure Reference Architecture center](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/batch-scoring-deep-learning), in this repository, we use the scenario of applying style transfer onto a video (collection of images). This architecture can be generalized for any batch scoring with deep learning scenario. An alternative solution using Azure Kubernetes Service can be found [here](https://github.com/Azure/Batch-Scoring-Deep-Learning-Models-With-AKS).

## Design
![Reference Architecture Diagram](https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/batchscoringdl-aml-architecture-diagram.jpg)

The above architecture works as follows:
1. Upload a video file to storage.
2. The video file will trigger Logic App to send a request to the AML pipeline published endpoint.
3. The pipeline will then process the video, apply style transfer with MPI, and postprocess the video.
4. The output will be saved back to blob storage once the pipeline is completed.

### What is Neural Style Transfer 

| Style image: | Input/content video: | Output video: | 
|--------|--------|---------|
| <img src="https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/style_image.jpg" width="300"> | [<img src="https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/input_video_image_0.jpg" width="300" height="300">](https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/input_video.mp4 "Input Video") *click to view video* | [<img src="https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/output_video_image_0.jpg" width="300" height="300">](https://happypathspublic.blob.core.windows.net/assets/batch_scoring_for_dl/output_video.mp4 "Output Video") *click to view* |

## Prerequsites

Local/Working Machine:
- Ubuntu >=16.04LTS (not tested on Mac or Windows)
- (Optional) [NVIDIA Drivers on GPU enabled machine](https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-18-04-bionic-beaver-linux) [Additional ref: [https://github.com/NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker)]
- [Conda >=4.5.4](https://conda.io/docs/)
- [AzCopy >=7.0.0](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-linux?toc=%2fazure%2fstorage%2ffiles%2ftoc.json)
- [Azure CLI >=2.0](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)

Accounts:
- [Azure Subscription](https://azure.microsoft.com/en-us/free/) 
- (Optional) A [quota](https://docs.microsoft.com/en-us/azure/azure-supportability/resource-manager-core-quotas-request) for GPU-enabled VMs

While it is not required, it is also useful to use the [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) to inspect your storage account.

## Setup

1. Clone the repo `git clone https://github.com/Azure/Batch-Scoring-Deep-Learning-Models-With-AML`
2. `cd` into the repo
3. Setup your conda env using the _environment.yaml_ file `conda env create -f environment.yml` - this will create a conda environment called __batchscoringdl_aml__
4. Activate your environment `conda activate batchscoringdl_aml`
5. Log in to Azure using the __az cli__ `az login`

## Steps
Run throught the following notebooks:
1. [Test the scripts](notebooks/01_local_testing.ipynb)
2. [Setup AML](notebooks/02_setup_aml.ipynb).
3. [Develop & publish AML pipeline](notebooks/03_develop_pipeline.ipynb)
4. [Deploy Logic Apps](notebooks/04_deploy_logic_apps.ipynb)
5. [Clean up](notebooks/05_clean_up.ipynb)

## Clean up
To clean up your working directory, you can run the `clean_up.sh` script that comes with this repo. This will remove all temporary directories that were generated as well as any configuration (such as Dockerfiles) that were created during the tutorials. This script will _not_ remove the `.env` file. 

To clean up your Azure resources, you can simply delete the resource group that all your resources were deployed into. This can be done in the `az cli` using the command `az group delete --name <name-of-your-resource-group>`, or in the portal. If you want to keep certain resources, you can also use the `az cli` or the Azure portal to cherry pick the ones you want to deprovision. Finally, you should also delete the service principle using the `az ad sp delete` command. 

All the step above are covered in the final [notebook](notebooks/05_clean_up.ipynb).

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
