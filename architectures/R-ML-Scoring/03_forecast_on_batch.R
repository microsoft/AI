
# 03_forecast_on_batch.R
# 
# This script generates forecasts for multiple products in parallel on Azure
# Batch. The doAzureParallel package schedules the jobs to be executed on the
# cluster and manages the job queue. Forecast results are written to blob.
#
# Run time ~5 minutes on a 5 node cluster

library(dotenv)
library(jsonlite)
library(doAzureParallel)
library(AzureStor)

source("R/utilities.R")
source("R/options.R")
source("R/create_credentials_json.R")
source("R/create_cluster_json.R")
source("R/create_features.R")
source("R/generate_forecast.R")


# Register batch pool and options for the job ----------------------------------

# If running from within docker container, recreate config files from
# environment variables.

if (!interactive()) {
  print("Creating config files")
  create_credentials_json()
  create_cluster_json()
}


# Set the doAzureParallel credentials

setCredentials("azure/credentials.json")


# Create the cluster

clust <- makeCluster("azure/cluster.json")


# Register the cluster as the doAzureParallel backend

registerDoAzureParallel(clust)

print(paste("Cluster has", getDoParWorkers(), "nodes"))


# Set doAzureParallel options

azure_options <- list(
  enableCloudCombine = TRUE,
  autoDeleteJob = FALSE
)


# Set packages to load on each node

pkgs_to_load <- c("dplyr", "gbm", "AzureStor")


# Get container object for reading/writing data

cont <- blob_container(
  get_env("BLOB_CONTAINER_URL"),
  key = get_env("STORAGE_ACCOUNT_KEY")
)


# Split product forecasts equally across nodes

chunks <- chunk_by_nodes(floor(TARGET_SKUS / INITIAL_SKUS))


# Generate forecasts
results <- foreach(
    idx=1:length(chunks),
    .options.azure = azure_options,
    .packages = pkgs_to_load
  ) %dopar% {
  
    
    models <- load_models("models", cont)
    
    products <- chunks[[idx]]
    
    for (product in products) {
      
      history <- read.csv(
          download_blob_file(
            paste0("data/history/product", product, ".csv"),
            cont
          )
        ) %>%
        select(sku, store, week, sales)
      
      futurex <- read.csv(
          download_blob_file(
            paste0("data/futurex/product", product, ".csv"),
            cont
          )
        )
      
      forecasts <- generate_forecast(
        futurex,
        history,
        models
      )
      
      upload_blob_file(
        forecasts,
        paste0("data/forecasts/product", product, ".csv"),
        cont = cont,
        quote = FALSE, row.names = FALSE)
      
    }
    
    TRUE
                         
  }


# Plot results to validate

if (interactive()) {
  library(ggplot2)
  library(dplyr)
  library(AzureStor)

  read.csv(
    download_blob_file("data/forecasts/product1.csv", cont)
  ) %>%
  filter(store == 2, sku %in% 1:4) %>%
  select(week, sku, q5:q95) %>%
  ggplot(aes(x = week)) +
  facet_grid(rows = vars(sku), scales = "free_y") +
  geom_ribbon(aes(ymin = q5, ymax = q95, fill = "q5-q95"), alpha = .25) + 
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = "q25-q75"), alpha = .25) +
  geom_line(aes(y = q50, colour = "q50"), linetype="dashed") +
  scale_y_log10() +
  scale_fill_manual(name = "", values = c("q25-q75" = "red", "q5-q95" = "blue")) +
  scale_colour_manual(name = "", values = c("q50" = "black")) +
  theme(
    axis.text.y=element_blank(),
    axis.ticks.y=element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  ) +
  labs(y = "forecast sales") +
  ggtitle(paste("Forecasts for SKUs 1 to 4 in store 2"))
}
