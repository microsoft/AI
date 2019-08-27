data(Boston, package="MASS")
if(!requireNamespace("randomForest")) install.packages("randomForest")
library(randomForest)

# train a model for median house price as a function of the other variables
model <- randomForest(medv ~ ., data=Boston, ntree=100)

# save the model
saveRDS(model, "data/model.rds")


# package up the model and container startup script into an image
library(AzureContainers)
call_docker("build -t mls-model .")
