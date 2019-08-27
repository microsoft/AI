model <- readRDS("model.rds")
score <- function(inputData)
{
    require(randomForest)
    inputData <- as.data.frame(inputData)
    predict(model, inputData)
}

library(mrsdeploy)

remoteLogin("http://localhost:12800", username="admin", password="Microsoft@2018", session=FALSE)
api <- publishService("mls-model", v="1.0.0",
    code=score,
    model=model,
    inputs=list(inputData="data.frame"),
    outputs=list(pred="vector"))
remoteLogout()
