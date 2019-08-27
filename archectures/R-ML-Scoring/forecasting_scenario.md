
### Forecasting scenario
This example uses the scenario of a large food retail company that needs to forecast the sales of thousands of products across multiple stores. A large grocery store can carry tens of thousands of products and generating forecasts for so many product/store combinations can be a very computationally intensive task.

### Dataset
This example uses the Orange Juice dataset from the *bayesm* R package which consists of just over two years' worth of weekly sales data for 11 orange juice SKUs (stock keeping units) across 83 stores. The data includes covariates including the price of each product, whether the product was on a deal or was featured in the store in each week. We expand this data through replication, resulting in 1,000 SKUs across 83 stores.
 
### Modelling approach
We show how trained GBM models (from the *gbm* R package) can be used to generate quantile forecasts with a forecast horizon of 13 weeks (1 quarter). Quantile forecasts allow for the uncertainty in the forecast to be estimated and in this example we generate five quantiles (the 5th, 25th, 50th, 75th and 95th percentiles). The total number of model scoring operations is 1,000 SKUs x 83 stores x 13 weeks x 5 quantiles = 5.4 million.