library(bayesm)
library(dplyr)
library(tidyr)

source("R/options.R")
source("R/utilities.R")


print("Extracting data from bayesm package...")

data("orangeJuice")

dat <- orangeJuice$yx

dat <- dat %>% 
  select(-c(constant, profit)) %>%
  mutate(feat = as.integer(feat))

print("Cleaning data...")


# Removing discontinued stores/brands

dat <- dat %>%
  merge(
    dat %>%
      group_by(store, brand) %>%
      summarise(max_week = max(week)) %>%
      filter(max_week == 160) %>%
      select(store, brand),
    all.y = TRUE
  )


# Reset store names

stores <- dat %>%
  select(store) %>%
  distinct()

stores$store_new <- as.integer(row.names(stores))

dat <- dat %>%
  merge(stores) %>%
  mutate(store = store_new) %>%
  select(-store_new)


# Set first week to be 0

dat$week <- dat$week - min(dat$week)


# Inserting records for missing time periods

get_stores_brands <- function(dat) {
  
  df <- dat %>%
    select(store, brand) %>%
    distinct()
  split(df, seq(nrow(df)))
  
}

insert_periods <- function(dat) {
  
  stores_brands <- get_stores_brands(dat)
  
  filled_dfs <- vector('list', length(stores_brands))
  
  for (i in 1:length(stores_brands)) {
    s <- stores_brands[[i]]$store
    b <- stores_brands[[i]]$brand
    df <- dat %>% filter(store == s, brand == b)
    weeks <- data.frame(week = min(df$week):max(df$week))
    weeks$store <- s
    weeks$brand <- b
    df <- df %>% merge(weeks, by = c('store', 'brand', 'week'), all.y = TRUE)
    filled_dfs[[i]] <- df
  }
  
  do.call(rbind, filled_dfs)
  
}

dat <- insert_periods(dat)


# Filling missing values

fill_time_series <- function(dat) {
  
  dat <- dat %>%
    group_by(store, brand) %>%
    arrange(week) %>%
    fill(-c(store, brand, week), .direction = "down") %>%
    ungroup()
  as.data.frame(dat)
  
}

dat <- fill_time_series(dat)


# Transform and rename variables

dat$sales <- exp(dat$logmove)
dat$logmove <- NULL

dat$sku <- dat$brand
dat$brand <- NULL

dat <- dat %>%
  select(
    sku,
    store,
    week,
    deal,
    feat,
    price1:price11,
    sales
  )


# Create data directories

create_dir("data")
create_dir("models")
create_dir(file.path("data", "futurex"))
create_dir(file.path("data", "history"))
create_dir(file.path("data", "forecasts"))
create_dir(file.path("data", "test"))


# Split dataset into history, future features and test sets

max_week <- max(dat$week)

dat %>%
  filter(week <= max_week - FORECAST_HORIZON) %>%
  arrange(sku, store, week) %>%
  write.csv(
    file.path("data", "history", "product1.csv"),
    quote = FALSE, row.names = FALSE
  )

dat %>%
  filter(week > max_week - FORECAST_HORIZON) %>%
  select(-c(sales)) %>%
  write.csv(
    file.path("data", "futurex", "product1.csv"),
    quote = FALSE, row.names = FALSE
  )

dat %>%
  filter(week > max_week - FORECAST_HORIZON) %>%
  write.csv(
    file.path("data", "test", "product1.csv"),
    quote = FALSE, row.names = FALSE
  )

rm(dat, orangeJuice, stores, max_week)
gc()

print("Done")
