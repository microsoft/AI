.ONESHELL:
SHELL=/bin/bash

define PROJECT_HELP_MSG
Makefile for testing notebooks
Make sure you have edited the dev_env_template files and renamed it to .dev_env
All the variables loaded in this makefile must come from the .dev_env file

Usage:
	make test					run all notebooks
	make clean					delete env and remove files
endef
export PROJECT_HELP_MSG
env_location=.dev_env
PWD:=$(shell pwd)
include ${env_location}


help:
	echo "$$PROJECT_HELP_MSG" | less


test: setup test-notebook1 test-notebook2 test-notebook3 test-notebook4 test-notebook5 test-notebook6 test-notebook7 \
	test-notebook-iot1 test-notebook8 test-notebook-iot2
	@echo All Notebooks Passed

setup:
	conda env create -f environment.yml
ifndef TENANT_ID
	@echo starting interactive login
	az login -o table
else
	@echo using service principal login
	az login -t ${TENANT_ID} --service-principal -u ${SP_USERNAME} --password ${SP_PASSWORD}
endif


test-notebook1:
	source activate deployment_aml
	@echo Testing 00_AMLSetup.ipynb
	papermill 00_AMLSetup.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p subscription_id ${SUBSCRIPTION_ID} \
		-p resource_group ${RESOURCE_GROUP} \
		-p workspace_name ${WORKSPACE_NAME} \
		-p workspace_region ${WORKSPACE_REGION} \
		-p image_name ${IMAGE_NAME} \
		-p aks_name ${AKS_NAME} \
		-p aks_location ${WORKSPACE_REGION} \
		-p aks_service_name ${AKS_SERVICE_NAME}

test-notebook2:
	source activate deployment_aml
	@echo Testing 01_DevelopModel.ipynb
	papermill 01_DevelopModel.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook3:
	source activate deployment_aml
	@echo Testing 02_DevelopModelDriver.ipynb
	papermill 02_DevelopModelDriver.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook4:
	source activate deployment_aml
	@echo Testing 03_BuildImage.ipynb
	papermill 03_BuildImage.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook5:
	source activate deployment_aml
	@echo Testing 04_DeployOnAKS.ipynb
	papermill aks/04_DeployOnAKS.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p aks_name ${AKS_NAME} \
		-p aks_location ${WORKSPACE_REGION} \
		-p aks_service_name ${AKS_SERVICE_NAME}

test-notebook6:
	source activate deployment_aml
	@echo Testing 05_TestWebApp.ipynb
	papermill aks/05_TestWebApp.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p aks_name ${AKS_NAME} \
		-p aks_location ${WORKSPACE_REGION} \
		-p aks_service_name ${AKS_SERVICE_NAME}

test-notebook7:
	source activate deployment_aml
	@echo Testing 06_SpeedTestWebApp.ipynb
	papermill aks/06_SpeedTestWebApp.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook-iot1:
	source activate deployment_aml
	@echo Testing 04_DeployOnIOTedge.ipynb
	export PYTHONPATH=${PWD}:${PYTHONPATH}
	cd iotedge
	papermill 04_DeployOnIOTedge.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p iot_hub_name fstlstnameiothub \
		-p device_id mygpudevice \
		-p module_name mygpumodule

test-notebook8:
	source activate deployment_aml
	@echo Testing 07_TearDown.ipynb
	papermill aks/07_TearDown.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook-iot2:
	source activate deployment_aml
	@echo Testing 05_TearDown.ipynb
	export PYTHONPATH=${PWD}:${PYTHONPATH}
	papermill iotedge/05_TearDown.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3


test-cookiecutter-aks:
	cookiecutter --no-input https://github.com/Microsoft/AKSDeploymentTutorialAML.git \
							subscription_id="${SUBSCRIPTION_ID}" \
							workspace_region=${WORKSPACE_REGION} \
							deployment_type="aks"

test-cookiecutter-iot:
	cookiecutter --no-input https://github.com/Microsoft/AKSDeploymentTutorialAML.git \
							subscription_id=${SUBSCRIPTION_ID} \
							workspace_region=${WORKSPACE_REGION} \
							deployment_type="iotedge"

remove-notebook:
	rm -f test.ipynb

clean: remove-notebook
	conda remove --name deployment_aml -y --all
	rm -rf aml_config
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints
	rm *.jpg
	rm -rf azureml-models
	rm driver.py img_env.yml model_resnet_weights.h5

notebook:
	source activate deployment_aml
	jupyter notebook --port 9999 --ip 0.0.0.0 --no-browser

install-jupytext:
	source activate deployment_aml
	conda install -c conda-forge jupytext

convert-to-py:
	jupytext --set-formats ipynb,py_scripts//py --sync *.ipynb

sync:
	jupytext --sync *.ipynb

convert-to-ipynb:
	jupytext --set-formats ipynb *.ipynb

remove-py:
	rm -r py_scripts

.PHONY: help test setup clean remove-notebook test-notebook1 test-notebook2 test-notebook3 test-notebook4 \
		test-notebook5 test-notebook6 test-notebook7 test-notebook-iot test-notebook9
