create_credentials_json <- function(save_dir = "azure",
                                    print_json = TRUE) {
  
  resource_id_prefix <- paste(
    "/subscriptions", get_env("SUBSCRIPTION_ID"), "resourceGroups",
    get_env("RESOURCE_GROUP"), "providers", sep = "/")
  
  batch_account_resource_id <- paste(
    resource_id_prefix, "Microsoft.Batch", "batchAccounts",
    get_env("BATCH_ACCOUNT_NAME"), sep = "/")
  
  storage_account_resource_id <- paste(
    resource_id_prefix, "Microsoft.Storage", "storageAccounts",
    get_env("STORAGE_ACCOUNT_NAME"), sep = "/")
  
  credentials <- list(
    servicePrincipal = list(
      tenantId = get_env("TENANT_ID"),
      storageEndpointSuffix = "core.windows.net",
      batchAccountResourceId = batch_account_resource_id,
      storageAccountResourceId = storage_account_resource_id,
      credential = get_env("SERVICE_PRINCIPAL_CRED"),
      clientId = get_env("SERVICE_PRINCIPAL_APPID")
    ),
    dockerAuthentication = list(
      "username" = get_env("REGISTRY_USERNAME"),
      "password" = get_env("REGISTRY_PASSWORD"),
      "registry" = get_env("REGISTRY_URL")
    )
  )
  
  credentials_json <- toJSON(credentials, auto_unbox = TRUE, pretty = TRUE)
  
  write(credentials_json, file = file.path(save_dir, "credentials.json"))
  
  if (print_json) print(credentials_json)
  
}