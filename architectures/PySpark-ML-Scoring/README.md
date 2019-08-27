# Batch scoring of Spark machine learning models 

## Overview

This scenario demonstrates batch scoring of a Spark machine learning model on Azure Databricks. We use a predictive maintenance scenario where we classify machine sensor readings to classify a set of four machine components into _healthy_ or _unhealthy requiring maintenance_ states. The resulting supervised multi-class classifier model scores batches of new observations through a regularly scheduled Azure Databricks notebook job.

The solution uses methods from the PySpark MLlib machine learning library, but the scoring process can be generalized to use any Spark, Python or R model hosted on Azure Databricks to make real-time predictions.

For an in-depth description of the scenario, we have documented the operations in each of the supplied Jupyter notebooks contained in the `./notebooks/` directory of this repository.

## Design

This solution uses the Azure Databricks service. We create jobs that set up the batch scoring demonstration. Each job executes a Databricks notebook to prepare the data and create the full solution. Within the architecture diagram below, each of the boxes represents a different job:

 1. **Ingest** downloads the simulated data sets from a GitHub site and converts and stores them as Spark dataframes on the Databricks DBFS. “Input Data” in the architecture diagram refers to a set of five simulated data sets related to realistic machine operating conditions.

 2. **Feature engineering** transforms and combines the data sets into an analysis data set. The analysis data set can be targeted for training a model or scoring data for a production pipeline. Each analysis data set is also stored in the Databricks DBFS.

 3. **Training** takes a subset of the complete data and constructs a model we can use to predict future outcomes. The model is stored in the Databricks DBFS for use by the scoring notebook.

 4. **Scoring** uses a different subset of the data, including data not yet collected to predict the current and future state of the machine. The model results are stored back onto the Databricks DBFS.

![Databricks Architecture diagram](./batch-scoring-spark.png "Architecture diagram")

# Prerequisites

 * We assume you have an Azure subscription. You will also need access to git on your working compute instance (local computer or VM). The repository is located at: `https://github.com/Azure/BatchSparkScoringPredictiveMaintenance`

* Any working computer that has a web browser, and runs python Python Version > 2.7.9 or > 3.6 as specified for using the Databricks CLI.

## Azure Databricks

This example is designed to run on [Azure Databricks](https://azure.microsoft.com/en-us/services/databricks/). Provision the service through your Azure subscription at the [Azure portal](https://portal.azure.com).

  * Click "+ Create a resource" button, then search for `databricks` and select the Azure Databricks search suggestion. Follow the prompts, and select `Standard pricing tier`. See https://azure.microsoft.com/en-us/pricing/details/databricks/ for information on different pricing tiers.
  
See https://docs.azuredatabricks.net/getting-started/index.html for detailed documentation on using Azure Databricks.

## Databricks cluster

Once your Azure Databricks service has been created, you will need to create a compute cluster to execute the notebooks.

  * From the portal, find your new Azure Databricks service, and `Launch Workspace`.
  * A new window will open in your browser. Select the *Clusters* icon, and click on the `+ Create Cluster` button to provision a new cluster. In the form that pops up, change the value of the `Python Version` dropdown menu to **3**. The remaining defaults values are acceptable.

## Databricks CLI

We will be using a Databricks command line utility (CLI) to automate running notebook tasks using the Databricks Jobs construct. Installing the Databricks CLI will simplify some of the operations required for this scenario. The first step is to import the Jupyter notebooks from the repository into your Databricks workspace. This can be accomplished with 1 command once the CLI is connected to your Azure Databricks instance.

From a command line, you can pip install the CLI using 

```
pip install --upgrade databricks-cli
```

# Setup

 * Clone the GitHub repository: 
 
 ```
 git clone https://github.com/Azure/BatchSparkScoringPredictiveMaintenance.git
 ```

 * `cd` into the root directory of your cloned repository

The next two subsections of this document detail how to:

 * Connect the CLI to your Databricks instance to simplify the import of repo notebooks.
 * Import the repo notebooks into your Databricks workspace

## Connect the CLI to your Databricks instance

We need to connect the CLI to your databricks instance. This can be done using a Databricks generated [Authentication token](https://docs.databricks.com/api/latest/authentication.html#token-management). This linking only needs to be done once.

 1. Copy the url portion of the web address of your Azure Databricks instance from your browser. You will not use the POST arguments for the hostname (everything including and following the '?' character). In `eastus` region, it will be `https://eastus.azuredatabricks.net/`.

 2. Create and copy an authentication token. Instructions are provided at the link above.

 3. From your working machine command line, `databricks configure --token`. This will prompt you for your Azure Databricks hostname and the authentication token.

## Import Notebooks

Use the CLI to copy the scenario notebooks to your Databricks instance. From your working machine command line, change into the local copy of the repository.  Then `databricks workspace import_dir [OPTIONS] SOURCE_PATH TARGET_PATH` 

  * The `SOURCE_PATH` will be the `./notebooks` directory. 
  * The `TARGET_PATH` will include your user name, which you can get from the Azure Databricks UI, it should be related to your Azure AD email of the form `<uname@example.com>`.  The whole `[TARGET_PATH]` should be of the form `/Users/<uname@example.com>/notebooks`.

The command should look like the following:

```{shell}
databricks workspace import_dir ./notebooks /Users/<uname@example.com>/notebooks
```

This will copy all required notebooks into the `notebooks` folder of your Azure Databricks Workspace.

To find these notebooks in your  Azure Databricks Workspace, use the *Workspace* icon, follow the path to your `/Users/<uname@example.com>/notebooks`. Databricks uses Jupyter notebooks with some extensions. Instructions on how to use Jupyter notebooks are at https://docs.databricks.com/user-guide/notebooks/notebook-use.html#run-notebooks.

# Steps

To create the full example scenario, log into your Azure Databricks workspace and run through the following notebooks that are now located there.

These notebooks need to be run sequentially in alpha-numeric order, as each depends on data artifacts produced in the previous notebooks full run.

When running the notebooks, you may have to start your Azure Databricks cluster or attach these notebooks to your Azure Databricks cluster. The UI will prompt you if this is required.

  * [Ingest Data](https://github.com/Azure/BatchSparkScoringPredictiveMaintenance/blob/master/notebooks/1_data_ingestion.ipynb). Open the `1_data_ingestion` notebook on the Azure Databricks workspace. You can either `Run All` cells, or execute cells individually. This notebook downloads the example data into your Azure Databricks Data storage.
  * [Model Training Pipeline](https://github.com/Azure/BatchSparkScoringPredictiveMaintenance/blob/master/notebooks/2_Training_Pipeline.ipynb) Open the `2_Training_Pipeline` notebook on the Azure Databricks workspace. You can either `Run All` cells, or execute cells individually. This notebook will run two external notebooks. 
      1. Create a training data set with `2a_feature_engineering`. The training data is written to the Azure Databricks Data store. Once this notebook is run, you can optionally examine the data created with the `2a_feature_exploration` notebook.
      2. Create a machine learning model with `2b_model_building`. Once this notebook is run, you can optionally examine the model with the `2b_model_testing` notebook with other data created with the `2a_feature_engineering` notebook. The model is stored on the Azure Databricks file system in parquet format.

  * [Data Scoring Pipeline](https://github.com/Azure/BatchSparkScoringPredictiveMaintenance/blob/master/notebooks/3_Scoring_Pipeline.ipynb) Open the `3_Scoring_Pipeline` notebook on the Azure Databricks workspace. You can either `Run All` cells, or execute cells individually. This notebook will also run two external notebooks. 

    1. Create a scoring data set with `2a_feature_engineering` with different input parameters than in the training dataset. The scoring data is written to the Azure Databricks Data store. Once this notebook is run, you can again optionally examine the data created with the `2a_feature_exploration` notebook. 
    2. `3a_model_scoring` will score the data with the machine learning model created with `2b_model_building`. The results data is written to the Azure Databricks Data store. Once this notebook is run, you can optionally examine the scored results data with the `3a_model_scoring_evaluation` notebook.
  * (optional) Instructions to create the batch scoring Databricks Job using the Databricks CLI are documented at https://github.com/Azure/BatchSparkScoringPredictiveMaintenance/blob/master/BatchScoringJob.md.

The scenario is constructed as a pipeline flow, where each notebook is optimized to perform in a batch setting for each of the ingest, feature engineering, model building, model scoring operations. To accomplish this, the feature engineering notebook is designed to be used to generate a general data set for any of the training, calibrate, test or scoring operations. In this scenario, we use a temporal split strategy for these operations, so the notebook parameters are used to set date range filtering.

# Conclusion

This scenario demonstrates how to automate the batch scoring of a predictive maintenance solution. The actual work of the "batch scoring a spark model" scenario is done through an Azure Databricks job. The job executes the `3_Scoring_Pipeline` notebook, which depends on a machine learning model existing on the Azure Databricks file storage. We created the model using the `2_Training_Pipeline` notebook which used the data downloaded with the `1_data_ingestion` notebook.

# Cleaning up

The easiest way to cleanup this work is to delete the resource group containing the Azure Databricks instance.

  1. Through the Azure portal (https://portal.azure.com) search for `databricks`.
  1. Open your Azure Databricks service and select the *Resource Group* link.
  1. *Delete resource group*  will remove the Azure Databricks service and all associated resources including the notebooks and data artifacts used in this scenario.

You may also want to remove the Databricks CLI from your python environment with

```{shell}
pip uninstall databricks-cli
```

# References

This scenario has been developed using a similar predictive maintenance use case published at following reference locations:

 * [Predictive Maintenance Solution Template](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance)
 * [Predictive Maintenance Modeling Guide](https://gallery.azure.ai/Collection/Predictive-Maintenance-Modelling-Guide-1)
 * [Predictive Maintenance Modeling Guide using SQL R Services](https://gallery.azure.ai/Tutorial/Predictive-Maintenance-Modeling-Guide-using-SQL-R-Services-1)
 * [Predictive Maintenance Modeling Guide Python Notebook](https://gallery.azure.ai/Notebook/Predictive-Maintenance-Modelling-Guide-Python-Notebook-1)
 * [Predictive Maintenance using PySpark](https://gallery.azure.ai/Tutorial/Predictive-Maintenance-using-PySpark)

We have also built an additional reference architecture leveraging spark for building real-time recommendation systems with off-line, pre-computed scores. These recommendation systems are common scenarios where scores are batch-processed. Relevant information about this related architecture is available here:

* [Build a real-time recommendation API on Azure](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/real-time-recommendation)
* [Technical details for recommendation systems](https://github.com/Microsoft/Recommenders)

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Author

John Ehrlinger <john.ehrlinger@microsoft.com>
