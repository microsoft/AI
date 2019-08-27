# Training Distributed Training on Batch AI

This repo is a tutorial on how to train a CNN model in a distributed fashion using Batch AI. 
The scenario covered is image classification, but the solution can be generalized for other deep learning scenarios such as segmentation and object detection. 

![Distributed training diagram](images/dist_training_diag2.png "Distributed training diagram")

Image classification is a common task in computer vision applications and is often tackled by training a convolutional neural network (CNN). 
For particularly large models with large datasets, the training process can take weeks or months on a single GPU. 
In some situations, the models are so large that it isn’t possible to fit reasonable batch sizes onto the GPU. 
Using distributed training in these situations helps shorten the training time. 
In this specific scenario, a ResNet50 CNN model is trained using Horovod on the ImageNet dataset as well as on synthetic data. 
The tutorial demonstrates how to accomplish this using three of the most popular deep learning frameworks: TensorFlow, Keras, and PyTorch.
There are number of ways to train a deep learning model in a distributed fashion, including data parallel and model parallel approaches based on synchronous and asynchronous updates. 
Currently the most common scenario is data parallel with synchronous updates—it’s the easiest to implement and sufficient for the majority of use cases. 
In data parallel distributed training with synchronous updates the model is replicated across N hardware devices and a 
mini-batch of training samples is divided into N micro-batches (see Figure 2). 
Each device performs the forward and backward pass for a micro-batch and when it finishes the process it shares the 
updates with the other devices. These are then used to calculate the updated weights of the entire mini-batch and then the 
weights are synchronized across the models. This is the scenario that is covered in the GitHub repository. The same architecture though can 
be used for model parallel and asynchronous updates.


## Prerequisites
* Computer with Nvidia GPU (The path was tested on an [Azure NC12 Ubuntu DSVM](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-gpu))
* Linux 
* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) installed
* [Nvidia Docker runtime](https://github.com/NVIDIA/nvidia-container-runtime) installed
* [Dockerhub](https://hub.docker.com/) account
* Port 9999 open on the VM or computer
* ImageNet dataset (look at [this](00_DataProcessing.ipynb) notebook for details)

## Setup 
Before you begin make sure you are logged into your dockerhub account by running on your machine:

```bash
docker login 
```



### Setup Execution Environment
Before being able to run anything you will need to set up the environment in which you will be executing the Batch AI commands etc. 
There are a number of dependencies therefore we offer a dockerfile that will take care of these dependencies for you. 
If you don't want to use Docker simply look inside the Docker directory at the dockerfile and environment.yml file for the dependencies. 
To build the container run(replace all instances of <dockerhub account> with your own dockerhub account name):

```bash
make build dockerhub=<dockerhub account>
```

The you run the command to start the environment (replace <data_location> with a location on your file system. Make sure it has at least 300GB of free space for the ImageNet dataset)
```bash
make jupyter dockerhub=<dockerhub account> data=<data_location>
```

This will start the Jupyter notebook on port 9999. Simply point your browser to the IP or DNS of your machine. 
From there you can navigate to [00_DataProcessing.ipynb](00_DataProcessing.ipynb) to process the ImageNet Data.

Once you have covered the two prerequisite notebooks folders [00_DataProcessing.ipynb](00_DataProcessing.ipynb) and [01_CreateResources.ipynb](01_CreateResources.ipynb)  you can 
navigate to the tutorials for each of the frameworks [HorovodTF](HorovodTF), [HorovodPytorch](HorovodPytorch) and [HorovodKeras](HorovodKeras).



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
