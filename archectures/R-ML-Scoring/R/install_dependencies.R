
# Install basic packages (from default cran mirror)

basic_pkgs <- c("devtools", "dotenv", "jsonlite")

install.packages(basic_pkgs)

repo <- "https://mran.microsoft.com/snapshot/2019-05-20"

pkgs <- c("bayesm", "dplyr", "tidyr", "ggplot2", "AzureStor", "AzureContainers", "AzureGraph")

install.packages(pkgs, repos = repo)

devtools::install_github(
  "Azure/rAzureBatch",
  ref = "1ab39ca1bb8ae589a6f5c80f5d91c1ee79b1ee8a" # 2019-28-14
)

devtools::install_github(
  "Azure/doAzureParallel",
  ref = "975858072e8194d465a1f63262e35815ebbf0306" # 2019-02-14
)

devtools::install_github(
  "gbm-developers/gbm",
  ref = "b59270a787202d7ba2de5f2af7032854691d2b10"
)

devtools::install_github(
  "Azure/AzureRMR",
  ref = "7407db42d38bf6a52b291ce8f9c2e3e7d4c9163f" # 2019-05-23
)
