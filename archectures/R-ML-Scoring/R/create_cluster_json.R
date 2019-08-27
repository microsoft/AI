create_cluster_json <- function(save_dir = "azure") {
  
  config <- list(
    name = get_env("CLUSTER_NAME"),
    vmSize = get_env("VM_SIZE"),
    maxTasksPerNode = 1,
    poolSize = list(
      dedicatedNodes = list(
        min = 0,
        max = as.integer(get_env("NUM_NODES"))
      ),
      lowPriorityNodes = list(
        min = 0,
        max = 0
      ),
      autoscaleFormula = "QUEUE_AND_RUNNING"
    ),
    containerImage = paste0(get_env("ACR_NAME"), ".azurecr.io/", get_env("WORKER_CONTAINER_IMAGE")),
    commandLine = c()
  )
  
  config_json <- toJSON(config, auto_unbox = TRUE, pretty = TRUE)
  
  write(config_json, file = file.path(save_dir, "cluster.json"))
  
}
