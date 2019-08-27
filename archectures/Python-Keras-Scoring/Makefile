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


include .dev_env


help:
	echo "$$PROJECT_HELP_MSG" | less


test: setup test-notebook1 test-notebook2 test-notebook3 test-notebook4 test-notebook5
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
	source activate batchscoringdl_aml
	cd notebooks 
	@echo Testing 01_local_testing.ipynb
	papermill 01_local_testing.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 

test-notebook2:
	source activate batchscoringdl_aml
	cd notebooks 
	@echo Testing 02_setup_aml.ipynb
	papermill 02_setup_aml.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p subscription_id ${SUBSCRIPTION_ID} \
		-p resource_group ${RESOURCE_GROUP} \
		-p workspace_name ${WORKSPACE_NAME} \
		-p workspace_region ${WORKSPACE_REGION} \
		-p storage_account_name ${STORAGE_ACCOUNT_NAME} 

test-notebook3:
	source activate batchscoringdl_aml
	cd notebooks 
	@echo Testing 03_develop_pipeline.ipynb
	papermill 03_develop_pipeline.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 

test-notebook4:
	source activate batchscoringdl_aml
	cd notebooks 
	@echo Testing 04_deploy_logic_apps.ipynb
	papermill 04_deploy_logic_apps.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 

test-notebook5:
	source activate batchscoringdl_aml
	cd notebooks 
	@echo Testing 05_clean_up.ipynb
	papermill 05_clean_up.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3  

remove-notebook: 
	rm -f notebooks/test.ipynb

clean: remove-notebook
	conda remove --name batchscoringdl_aml -y --all
	cd notebooks
	./clean_up.sh
	rm -rf aml_config
	rm -rf aml_test_orangutan
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints

.PHONY: help test setup clean remove-notebook test-notebook1 test-notebook2 test-notebook3 test-notebook4 test-notebook5