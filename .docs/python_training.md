# Azure services for training Python ML models

<p align="center">
  <img width="800" src="../images/python_training_diag.png">
</p>

There are many options for training ML models in Python on Azure. The most straight forward way is to train your model on a [DSVM](https://azure.microsoft.com/en-us/services/virtual-machines/data-science-virtual-machines/). You can either do this in local model straight on the VM or through attaching it in AzureML as a compute target. If you want to have AzureML manage the compute for you and scale it up and down based on whether jobs are waiting in the queue, then you should AzureML Compute. 

Now if you are going to run multiple jobs for hyperparameter tuning or other purposes then we would recommend using [Hyperdrive](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-tune-hyperparameters), [Azure automated ML](https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-automated-ml) or AzureML Compute dependent on your requirements.
For a tutorial on how to use Hyperdrive go [here](https://github.com/Microsoft/MLHyperparameterTuning).
