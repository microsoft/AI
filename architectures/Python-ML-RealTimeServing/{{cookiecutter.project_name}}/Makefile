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
	test-notebook8 test-notebook-iot1 test-notebook9 test-notebook-iot2
	@echo All Notebooks Passed

setup:
	conda env create -f environment.yml
ifndef TENANT_ID
	@echo starting interactive login
	az login -o table
	az account set --subscription ${SUBSCRIPTION_ID}
else
	@echo using service principal login
	az login -t ${TENANT_ID} --service-principal -u ${SP_USERNAME} --password ${SP_PASSWORD}
endif


test-notebook1:
	source activate MLAKSDeployAML
	@echo Testing 00_AMLConfiguration.ipynb
	papermill 00_AMLConfiguration.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p subscription_id ${SUBSCRIPTION_ID} \
		-p resource_group ${RESOURCE_GROUP} \
		-p workspace_name ${WORKSPACE_NAME} \
		-p workspace_region ${WORKSPACE_REGION} \
		-p image_name ${IMAGE_NAME} \

test-notebook2:
	source activate MLAKSDeployAML
	@echo Testing 01_DataPrep.ipynb
	papermill 01_DataPrep.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook3:
	source activate MLAKSDeployAML
	@echo Testing 02_TrainOnLocal.ipynb
	papermill 02_TrainOnLocal.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook4:
	source activate MLAKSDeployAML
	@echo Testing 03_DevelopScoringScript.ipynb
	papermill 03_DevelopScoringScript.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3
	sleep 1m

test-notebook5:
	source activate MLAKSDeployAML
	@echo Testing 04_CreateImage.ipynb
	papermill 04_CreateImage.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3
	sleep 30

test-notebook6:
	source activate MLAKSDeployAML
	@echo Testing 05_DeployOnAKS.ipynb
	papermill aks/05_DeployOnAKS.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p aks_name ${AKS_NAME} \
		-p aks_location ${WORKSPACE_REGION} \
		-p aks_service_name ${AKS_SERVICE_NAME}

test-notebook7:
	source activate MLAKSDeployAML
	@echo Testing 06_SpeedTestWebApp.ipynb
	papermill aks/06_SpeedTestWebApp.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3
        
test-notebook8:
	source activate MLAKSDeployAML
	@echo Testing 07_RealTimeScoring.ipynb
	papermill aks/07_RealTimeScoring.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3
        

test-notebook-iot1:
	source activate MLAKSDeployAML
	@echo Testing 05_DeployOnIOTedge.ipynb
	export PYTHONPATH=${PWD}:${PYTHONPATH}
	cd iotedge
	mkdir ./data_folder
	cp ../data_folder/dupes_test.tsv ./data_folder
	papermill 05_DeployOnIOTedge.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p iot_hub_name fstlstnameiothub \
		-p device_id mydevice \
		-p module_name mymodule

test-notebook9:
	source activate MLAKSDeployAML
	@echo Testing 08_TearDown.ipynb
	papermill aks/08_TearDown.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook-iot2:
	source activate MLAKSDeployAML
	@echo Testing 06_TearDown.ipynb
	export PYTHONPATH=${PWD}:${PYTHONPATH}
	papermill iotedge/06_TearDown.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3


test-cookiecutter-aks:
	cookiecutter --no-input https://github.com/Microsoft/MLAKSDeployAML.git --checkout yzhang \
							subscription_id="${SUBSCRIPTION_ID}" \
							workspace_region=${WORKSPACE_REGION} \
							deployment_type="aks"

test-cookiecutter-iot:
	cookiecutter --no-input https://github.com/Microsoft/MLAKSDeployAML.git --checkout yzhang \
							subscription_id=${SUBSCRIPTION_ID} \
							workspace_region=${WORKSPACE_REGION} \
							deployment_type="iotedge"

remove-notebook:
	rm -f test.ipynb

clean: remove-notebook
	conda remove --name MLAKSDeployAML -y --all
	rm -rf aml_config
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints
	rm -rf data_folder
	rm -rf azureml-models
	rm -rf score.py lgbmenv.yml model.pkl
	rm -rf iotedge/deployment.json iotedge/deviceconfig.sh
	rm -rf iotedge/data_folder

notebook:
	source activate MLAKSDeployAML
	jupyter notebook --port 9999 --ip 0.0.0.0 --no-browser

install-jupytext:
	source activate MLAKSDeployAML
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
		test-notebook5 test-notebook6 test-notebook7 test-notebook8 test-notebook-iot1 test-notebook9 test-notebook-iot2
