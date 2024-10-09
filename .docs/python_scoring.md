# Azure services for deploying Python ML

<p align="center">
  <img width="800" src="../images/decision_python_scoring.png">
</p>

When deploying ML models in Python there are two core questions. The first question is will it be real time and the second is whether the model is a deep learning model. For deploying deep learning models that require real time we recommend Azure Kubernetes Services (AKS) with GPUs. For a tutorial on how to do that look at [AKS w/GPU](https://github.com/Microsoft/AKSDeploymentTutorialAML). For deploying deep learning models for batch scoring we recommend using AzureML pipelines with GPUs, for a tutorial on how to do that look [AzureML Pipelines w/GPU](https://github.com/Azure/Batch-Scoring-Deep-Learning-Models-With-AML). For non deep learning models we recommend you use the same services but without GPUs. For a tutorial on deploying classical ML models for real time scoring look [AKS](https://github.com/Microsoft/MLAKSDeployAML) and for batch scoring [AzureML Pipelines](https://github.com/Microsoft/AMLBatchScoringPipeline)
