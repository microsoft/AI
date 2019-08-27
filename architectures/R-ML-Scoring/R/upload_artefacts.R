
library(AzureRMR)
library(AzureStor)

source("R/options.R")
source("R/utilities.R")

key <- Sys.getenv("HAPPYPATHSKEY")

ep <- blob_endpoint(
  "https://happypathspublic.blob.core.windows.net",
  key = key)

list_blob_containers(ep)

assets <- blob_container(ep, "assets")

list_blobs(assets)


# Delete existing models

model_names <- list_model_names(list_required_models(6, QUANTILES))
lapply(model_names, function(m) {
    delete_blob(assets, paste0("batch_forecasting/models", m), confirm = FALSE)
  })


# Upload new models

run(
  "azcopy --source %s --destination %s --dest-key %s --recursive --quiet",
  "models",
  file.path(
    "https://happypathspublic.blob.core.windows.net",
    "assets", "batch_forecasting", "models"
  ),
  key
)

list_blobs(assets)


# Upload images -----------------------------------------------------------

upload_to_url(
  src = "forecasts.png",
  dest = file.path(
    "https://happypathspublic.blob.core.windows.net",
    "assets", "batch_forecasting", "images", "forecasts.png"
  ),
  key = key
)


upload_to_url(
  src = "architecture.png",
  dest = file.path(
    "https://happypathspublic.blob.core.windows.net",
    "assets", "batch_forecasting", "images", "architecture.png"
  ),
  key = key 
)

list_blobs(assets)
