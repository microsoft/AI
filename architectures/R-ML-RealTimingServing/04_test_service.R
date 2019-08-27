source("resource_specs.R")


ingr_uri <- paste0("https://mls-model.", rg_loc, ".cloudapp.azure.com/")

# need to configure the curl handle to ignore warning about an untrusted cert
unverified_handle <- function()
{
    structure(list(
        handle=curl::handle_setopt(curl::new_handle(), ssl_verifypeer=FALSE),
        url=ingr_uri),
    class="handle")
}

# get login token: use same username/password as when creating the service
response <- httr::POST(paste0(ingr_uri, "login"),
    body=list(username="admin", password="Microsoft@2018"),
    encode="json",
    handle=unverified_handle())
token <- httr::content(response)$access_token


# get predictions for a sample of rows
# MMLS Model Operationalization generates verbose output; consult the documentation for more details
newdata <- jsonlite::toJSON(list(inputData=MASS::Boston[1:10,]), dataframe="columns")
response <- httr::POST(paste0(ingr_uri, "api/mls-model/1.0.0"),
    httr::add_headers(Authorization=paste0("Bearer ", token),
        `content-type`="application/json"),
    body=newdata,
    handle=unverified_handle())
httr::content(response, simplifyVector=TRUE)


# swagger file (if needed, eg for Azure API Management)
response <- httr::GET(paste0(ingr_uri, "api/mls-model/1.0.0/swagger.json"),
    httr::add_headers(Authorization=paste0("Bearer ", token),
        `content-type`="application/json"),
    handle=unverified_handle())
cat(httr::content(response))
