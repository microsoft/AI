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
