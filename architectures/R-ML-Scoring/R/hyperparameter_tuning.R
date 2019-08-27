
# hyperparameter_tuning.R
# 
# This script finds an appropriate set of hyperparameters for the t+1 GBM model

library(dotenv)
library(jsonlite)
library(dplyr)
library(doAzureParallel)
library(caret)
library(ggplot2)

source("R/utilities.R")
source("R/options.R")
source("R/create_credentials_json.R")
source("R/create_cluster_json.R")
source("R/create_features.R")


# Register batch pool and options for the job ----------------------------------

setCredentials("azure/credentials.json")
clust <- makeCluster("azure/cluster.json")
registerDoAzureParallel(clust)
getDoParWorkers()
azure_options <- list(
  enableCloudCombine = TRUE,
  autoDeleteJob = FALSE
)
file_dir <- "/mnt/batch/tasks/shared/files"
pkgs_to_load <- c("dplyr", "gbm")


# Compute baselines -------------------------------------------------------

# Load small dataset

dat <- read.csv(file.path("data", "history", "product1.csv")) %>%
  bind_rows(
    read.csv(file.path("data", "test", "product1.csv"))
  )

# Define test period and validation period start

test_start <- 108


# Compute the mean forecast (mean of all previous values), as the baseline

mape <- function(forecasts, actuals) {mean(abs(forecasts - actuals) / actuals)}

baseline <- dat %>%
  select(sku, store, week, sales) %>%
  arrange(sku, store, week) %>%
  group_by(sku, store) %>%
  mutate(
    cum_mean = cummean(sales),
    mean_forecast = lag(cum_mean),
    lag1_forecast = lag(sales, n = 1),
    lag4_forecast = lag(sales, n = 4),
    lag8_forecast = lag(sales, n = 8),
    lag12_forecast = lag(sales, n = 12)
  ) %>%
  filter(week >= test_start) %>%
  ungroup() %>%
  filter(complete.cases(.)) %>%
  summarise(
    mean_forecast = mape(mean_forecast, sales),
    lag1_forecast = mape(lag1_forecast, sales),
    lag4_forecast = mape(lag4_forecast, sales),
    lag8_forecast = mape(lag8_forecast, sales),
    lag12_forecast = mape(lag12_forecast, sales)
  )

baseline


# Tune t+1 model hyperparameters ----------------------------------------------

dat <- create_features(dat, step = 1, remove_target = FALSE)


# Split training and test sets

train <- dat %>% filter(week < test_start) %>% as.data.frame(.)
test <- dat %>% filter(week >= test_start) %>% as.data.frame(.)


# Specify training and validation fold indices

fold_weeks_in <- list(
  0:(test_start - (FORECAST_HORIZON * 3) - 1),
  0:(test_start - (FORECAST_HORIZON * 2) - 1),
  0:(test_start - FORECAST_HORIZON - 1)
)
fold_weeks_out <- list(
  (test_start - (FORECAST_HORIZON * 3)):(test_start - (FORECAST_HORIZON * 2) - 1),
  (test_start - (FORECAST_HORIZON * 2)):(test_start - FORECAST_HORIZON - 1),
  (test_start - FORECAST_HORIZON):(test_start - 1)
)

fold_idx_in <- list(
  as.integer(row.names(train[train$week %in% fold_weeks_in[[1]], ])),
  as.integer(row.names(train[train$week %in% fold_weeks_in[[2]], ])),
  as.integer(row.names(train[train$week %in% fold_weeks_in[[3]], ]))
)

fold_idx_out <- list(
  as.integer(row.names(train[train$week %in% fold_weeks_out[[1]], ])),
  as.integer(row.names(train[train$week %in% fold_weeks_out[[2]], ])),
  as.integer(row.names(train[train$week %in% fold_weeks_out[[3]], ]))
)


# Tune gbm hyperparameters

fit_control <- trainControl(
  method = "cv",
  index = fold_idx_in,
  indexOut = fold_idx_out,
  allowParallel = TRUE,
  savePredictions = FALSE,
  returnData = FALSE
)

gbm_grid <-  expand.grid(
  interaction.depth = c(5, 10, 15, 20),
  n.trees = seq(500, 3000, 250),
  shrinkage = c(0.01, 0.05, 0.1),
  n.minobsinnode = c(10)
)

# gbm_grid <-  expand.grid(
#   interaction.depth = c(15),
#   n.trees = c(1000),
#   shrinkage = c(0.01),
#   n.minobsinnode = c(10)
# )

form <- as.formula(
  paste("sales ~ sku + deal + feat + level +",
        "month_mean + month_max + month_min + lag1 +",
        paste(paste0("price", 1:11), collapse = " + ")
  )
)

system.time({
  gbm_fit <- train(form,
                   data = train,
                   method = "gbm",
                   distribution = "gaussian",
                   tuneGrid = gbm_grid,
                   trControl = fit_control, 
                   verbose = FALSE)
})


# Inspect the tuning results

param_results <- gbm_fit$results %>% arrange(MAE)
View(param_results)

ggplot(gbm_fit)


# Fix the hyperparameters

N.TREES <- 1250
INTERACTION.DEPTH <-20
SHRINKAGE <- 0.05
N.MINOBSINNODE <- 10


# Evaluate the final model on test set

mape(exp(predict(gbm_fit, test, n.trees = gbm_fit$n.trees)), exp(test$sales))
