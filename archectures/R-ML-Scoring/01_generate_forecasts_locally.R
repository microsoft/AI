
# 01_generate_forecasts_locally.R
# 
# This script extracts product sales data from the bayesm R package. The data
# consists of weekly sales of 11 orange juice brands across 83 stores. Forecasts
# are generated for these products using pre-trained models.
#
# Note: As with all scripts in this repository, it is recommended that you step
# through it line-by-line (with Ctrl + Enter if using RStudio)
#
# Run time ~2 minutes

library(dplyr)
library(gbm)
library(ggplot2)
library(AzureStor)

source("R/utilities.R")
source("R/options.R")


# Extract data -----------------------------------------------------------------

# Extract and preprocess data from bayesm package

source("R/get_data.R")


# Explore data -----------------------------------------------------------------

dat <- read.csv(file.path("data", "history", "product1.csv"))


# Plot quantiles of total weekly sales (for all products) by store. The sales
# vary significantly across stores, and from week to week.

dat %>%
  group_by(week, store) %>%
  summarise(sales = sum(sales)) %>%
  group_by(week) %>%
  summarise(
    q5 = quantile(sales, probs = 0.05),
    q25 = quantile(sales, probs = 0.25),
    q50 = quantile(sales, probs = 0.5),
    q75 = quantile(sales, probs = 0.75),
    q95 = quantile(sales, probs = 0.95)
  ) %>%
  ggplot(aes(x = week)) +
  geom_ribbon(aes(ymin = q5, ymax = q95, fill = "5%-95%"), alpha = .25) + 
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = "25%-75%"), alpha = .25) +
  geom_line(aes(y = q50, colour = "q50")) +
  scale_y_log10() +
  scale_fill_manual(name = "", values = c("25%-75%" = "red", "5%-95%" = "blue")) +
  scale_colour_manual(name = "", values = c("q50" = "black")) +
  labs(y = "total sales by store") +
  ggtitle("Quantiles of total sales by store")


# Plot total weekly sales by SKU (stock keeping unit of each orange juice brand).
# The total sales of each product varies significantly week to week and also
# between products.

dat %>%
  mutate(sku = as.factor(sku)) %>%
  group_by(sku, week) %>%
  summarise(sales = sum(sales)) %>%
  ggplot(aes(x = sku, y =sales, colour = sku)) +
  geom_boxplot() +
  scale_y_log10() +
  labs(y = "Total weekly sales") +
  ggtitle("Total weekly sales by SKU")


# Generate a forecast ----------------------------------------------------------

# Download pre-trained models from blob storage. We are forecasting 13 time
# steps (weeks) into the future and generating predictions for 5 quantiles
# (5%, 25%, 50%, 75% and 95%). A separate model has been trained for each time
# step and quantile combination for time steps 1 to 6. For time steps 7 to 13, a
# single model per quantile has been trained. There are 35 individual models
# in total.

create_dir("models")

cont <- blob_container("https://happypathspublic.blob.core.windows.net/assets")

multidownload_blob(
  cont,
  src = "/batch_forecasting/models/*",
  dest = "models",
  overwrite = TRUE
)


# List the downloaded models. Note that models for t7 (time step 7) will be
# applied to all time steps from 7 to 13.

list.files("models")


# Define function for creating model features

create_features <- function(dat,
                            step = 1,
                            remove_target = TRUE,
                            filter_week = NULL) {
  
  # Computes features from product sales history including the most recent
  # observed value (lag1), the mean, max and min values of the previous
  # month, and the mean weekly sales by store (level).
  #
  # Args:
  #   dat:  dataframe containing historical sales values by sku and store.
  #   step: the time step to be forecasted. This determines how far the lagged
  #         features are shifted.
  #   remove_target: remove the target variable (sales) from the result.
  #   filter_week: filter result for the specified week
  #
  # Returns:
  #   A dataframe of model features
  
  
  dat %>%
    arrange(sku, store, week) %>%
    group_by(sku, store) %>%
    mutate(
      sales = log(sales),
      lag1 = lag(sales, n = 1 + step - 1),
      lag2 = lag(sales, n = 2 + step - 1),
      lag3 = lag(sales, n = 3 + step - 1),
      lag4 = lag(sales, n = 4 + step - 1),
      lag5 = lag(sales, n = 5 + step - 1),
      month_mean = (lag1 + lag2 + lag3 + lag4 + lag5) / 5,
      month_max = pmax(lag1, lag2, lag3, lag4, lag5),
      month_min = pmin(lag1, lag2, lag3, lag4, lag5)
    ) %>%
    group_by(sku, store, isna = is.na(lag1)) %>%
    mutate(level = ifelse(isna, NA, cummean(lag1))) %>%
    ungroup() %>%
    {if (remove_target) select(., -c(sales)) else select_all(.)} %>%
    {if (!is.null(filter_week)) filter(., week == filter_week) else select_all(.)} %>%
    filter(complete.cases(.)) %>%
    select(-c(isna, lag2:lag5))
  
}


# Write function definition to file

write_function(create_features, "R/create_features.R")


# Define forecast scoring function

generate_forecast <- function(futurex,
                              history,
                              models,
                              transform_predictions = TRUE) {
  
  # Generates quantile forecasts with a horizon of 13 weeks for each sku of
  # a product.
  #
  # Args:
  #   futurex: feature dataset for forecast period
  #   history: sales history for all SKUs
  #   models: a list of trained gbm models for each time step and quantile
  #   transform_predictions: transform the forecast from log sales to sales
  #
  # Returns:
  #   A dataframe of quantile forecasts
  

  generate_quantile_forecast <- function(q, model_idx, dat) {
    
    # Retrieve time step- and quantile-specific model
    
    model_name <- paste0(
      "gbm_t", as.character(model_idx),
      "_q", as.character(100 * q)
    )
    model <- models[[model_name]]$model
    
    
    # Make the prediction
    
    pred <- predict(model, dat, n.trees = model$n.trees)
    
    
    # Convert back to sales from log sales
    
    if (transform_predictions) pred <- exp(pred)
    
    pred
    
  }
  
  
  generate_step_forecasts <- function(step) {
    
    # Create features specific to the required time step
    
    step_features <- create_features(
      features, step = step,
      remove_target = TRUE,
      filter_week = forecast_start_week + step - 1
      )
    step_features$step <- step

    
    # Specify which time step model to use
    
    if (step <= 6) model_idx <- step else model_idx <- 7
    
    
    # Generate the quantile forecasts
    
    quantile_forecasts <- lapply(
      QUANTILES,
      generate_quantile_forecast,
      model_idx,
      step_features
    )
  
    
    quantile_forecasts <- as.data.frame(quantile_forecasts)
    colnames(quantile_forecasts) <-  paste0("q", as.character(QUANTILES * 100))
    
    # Sort to avoid crossing quantiles
    
    t(apply(quantile_forecasts, 1, sort))
    
    cbind(step_features, quantile_forecasts)
    
  }
  
  
  # Combine futurex and history into one feature dataset
  
  features <- bind_rows(futurex, history)
  
  
  # Generate forecasts over the 13 steps of the forecast period
  
  steps <- 1:FORECAST_HORIZON
  forecast_start_week <- min(futurex$week)
  
  step_forecasts <- lapply(steps, generate_step_forecasts)
  
  do.call(rbind, step_forecasts) %>% arrange(sku, store, week)
  
}


write_function(generate_forecast, "R/generate_forecast.R")


# Load trained models

models <- load_models()


# Load forecast period features and sales history data

history <- read.csv(
    file.path("data", "history",
              paste0("product1.csv"))
  ) %>%
  select(sku, store, week, sales)
  
futurex <- read.csv(
    file.path("data", "futurex",
              paste0("product1.csv"))
  )


# Generate a forecast for all 11 SKUs

forecasts <- generate_forecast(futurex, history, models)


# Plot the forecast output of four SKUs in one store. You can ignore the warning
# about missing values

plot_store <- 1

dat %>%
  filter(store == plot_store, sku %in% 1:4, week >= 80, week < 108) %>%
  select(week, sku, sales) %>%
  bind_rows(
    forecasts %>%
      filter(store == plot_store, sku %in% 1:4) %>%
      select(week, sku, q5:q95)
  ) %>%
  ggplot(aes(x = week)) +
  facet_grid(rows = vars(sku), scales = "free_y") +
  geom_ribbon(aes(ymin = q5, ymax = q95, fill = "q5-q95"), alpha = .25) + 
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = "q25-q75"), alpha = .25) +
  geom_line(aes(y = q50, colour = "q50"), linetype="dashed") +
  geom_line(aes(y = sales)) +
  scale_y_log10() +
  scale_fill_manual(name = "", values = c("q25-q75" = "red", "q5-q95" = "blue")) +
  scale_colour_manual(name = "", values = c("q50" = "black")) +
  theme(
    axis.text.y=element_blank(),
    axis.ticks.y=element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  ) +
  labs(y = "sales") +
  ggtitle(paste("Forecasts for SKUs 1 to 4 in store 1")) +
  ggsave("images/forecasts.png", device = "png", width = 7, height = 7)

