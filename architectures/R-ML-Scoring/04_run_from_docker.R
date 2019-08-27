
# 04_run_from_docker.R
# 
# This script defines a docker image for the job scheduler. The forecast
# generation process is then triggered from a docker container running locally.
#
# Run time ~5 minutes on a 5 node cluster


# Define docker image ----------------------------------------------------------

# The dockerfile used to build to the scheduler docker image can be reviewed in
# docker/scheduler/dockerfile

library(dotenv)
library(AzureContainers)
source("R/utilities.R")


registry <- AzureRMR::get_azure_login(get_env("TENANT_ID"))$
  get_subscription(get_env("SUBSCRIPTION_ID"))$
  get_resource_group(get_env("RESOURCE_GROUP"))$
  get_acr(get_env("ACR_NAME"))$
  get_docker_registry()


scheduler <- get_env("SCHEDULER_CONTAINER_IMAGE")

# Build scheduler docker image

call_docker(sprintf("build -t %s -f docker/scheduler/dockerfile .", scheduler))


# Push the image to Docker Hub

registry$push(scheduler)


# Run the docker container

env_vars <- get_dotenv_vars()

call_docker(paste("run", paste0("-e ", env_vars, "=", get_env(env_vars), collapse = " "), scheduler))
