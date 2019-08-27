

# doAzureParallel utils --------------------------------------------------------

chunk_by_nodes <- function(multiplier) {
  
  num_nodes <- as.numeric(get_env("NUM_NODES"))
  reps <- rep(1:num_nodes, each=multiplier/num_nodes)
  reps <- c(reps, rep(max(reps), multiplier - length(reps)))
  chunks <- split(1:multiplier, reps)
  chunks
  
}


terminate_all_jobs <- function() {
  jobs <- getJobList()
  job_ids <- jobs$Id
  lapply(job_ids, terminateJob)
}


delete_all_jobs <- function() {
  jobs <- getJobList()
  job_ids <- jobs$Id
  lapply(job_ids, deleteJob)
}


delete_cluster <- function(cluster) {
  stopCluster(cluster)
  print("Waiting for cluster deletion..")
  status <- "deleting"
  while(!is.null(status)) {
    Sys.sleep(5)
    clusters <- getClusterList()
    status <- clusters[clusters$Id == get_env("CLUSTER_NAME")]$State
  }
  print("Cluster deleted")
}


# Data utils -------------------------------------------------------------------

load_data <- function(path = ".") {
  files <- lapply(list.files(path, full.names = TRUE), read.csv)
  dat <- do.call("rbind", files)
}


download_blob_file <- function(f, cont) {
  tmpfile <- tempfile()
  download_blob(cont, src = f, dest = tmpfile)
  tmpfile
}


upload_blob_file <- function(x, f, cont, ...) {
  tmpfile <- tempfile()
  write.csv(x, tmpfile, ...)
  upload_blob(cont, src = tmpfile, dest = f)
}


# Model utils -------------------------------------------------------------

load_model <- function(name, path, cont = NULL) {
  
  f <- file.path(path, name)
  if (!is.null(cont)) {
    tmpfile <- download_blob_file(f, cont)
    f <- tmpfile
  }
  list(name = name, model = readRDS(f))
  
}


load_models <- function(path = "models", cont = NULL) {
  
  model_names <-list_model_names(
    list_required_models(lagged_feature_steps = 6, quantiles = QUANTILES)
  )
  
  models <- lapply(model_names, load_model, path, cont)
  names(models) <- model_names
  models
  
}


list_required_models <- function(lagged_feature_steps, quantiles) {
  required_models <- expand.grid(1:(lagged_feature_steps + 1), quantiles)
  colnames(required_models) <- c("step", "quantile")
  split(required_models, seq(nrow(required_models)))
}


list_model_names <- function(required_models) {
  lapply(
    required_models,
    function(model) {
      paste0(
        "gbm_t", as.character(model$step), "_q",
        as.character(model$quantile * 100)
      )
    }
  )
}


# System utils ------------------------------------------------------------

create_dir <- function(path) if (!dir.exists(path)) dir.create(path)


run <- function(cmd, ..., test = FALSE, intern = FALSE) {
  args <- list(...)
  print(do.call(sprintf, c(cmd, args)))
  if (!test) {
    system(do.call(sprintf, c(cmd, args)), intern = intern)
  }
}


write_function <- function(fn, file) {
  fn_name <- deparse(substitute(fn))
  fn_capture <- capture.output(print(fn))
  fn_capture[1] <- paste0(fn_name, " <- ", fn_capture[1])
  writeLines(fn_capture, file)
}


set_env <- function(name, value, dotenv_file = ".env") {
  
  # Remove existing entry in .env file
  rm_env(name, dotenv_file)
  
  # Add variable to .env file
  txt <- paste(name, value, sep = "=")
  write(txt, file = dotenv_file, append = TRUE)
  
  # Reload all vars into R session
  load_dot_env(dotenv_file)
}


unset_env <- function(var, dotenv_file = ".env") {
  Sys.unsetenv(var)
  rm_env(var, dotenv_file)
}


get_env <- function(var) {
  Sys.getenv(var)
}


get_dotenv_vars <- function(dotenv_file = ".env") {
  dotenv_lines <- read_dotenv(dotenv_file)
  dotenv_lines_to_vars(dotenv_lines)
}


rm_env <- function(var, dotenv_file = ".env") {
  if (!file.exists(dotenv_file)) return(invisible())
  dotenv_lines <- read_dotenv(dotenv_file)
  if (length(dotenv_lines)) {
    dotenv_vars <- dotenv_lines_to_vars(dotenv_lines)
    lines_to_remove <- which(find_dotenv_var(dotenv_vars, var))
    if (length(lines_to_remove)){
      dotenv_lines <- dotenv_lines[-lines_to_remove]
      if (length(dotenv_lines)) {
        write(dotenv_lines, file = dotenv_file, append = FALSE)
      } else {
        close(file(dotenv_file, open="w"))
      }
    }
  }
}


dotenv_lines_to_vars <- function(dotenv_lines) {
  unlist(
    lapply(dotenv_lines, function(x) strsplit(x, "=")[[1]][1])
  )
}


find_dotenv_var <- function(dotenv_vars, var) {
  unlist(
    lapply(
      dotenv_vars, function(dotenv_var) dotenv_var == var
    )
  )
}


read_dotenv <- function(dotenv_file = ".env") {
  readLines(dotenv_file)
}


set_resource_specs <- function(dotenv_file = ".env") {
  
  # Create or replace a .env file to hold secrets
  invisible({
    if (file.exists(dotenv_file)) file.remove(dotenv_file)
    file.create(dotenv_file)
  })
  
  source("00_resource_specs.R")
  
  expected_envs <- c(
    "SUBSCRIPTION_ID",
    "TENANT_ID",
    "ACR_NAME",
    "REGION",
    "RESOURCE_GROUP",
    "SERVICE_PRINCIPAL_NAME",
    "BATCH_ACCOUNT_NAME",
    "STORAGE_ACCOUNT_NAME",
    "BLOB_CONTAINER_NAME",
    "LOGIC_APP_NAME",
    "ACI_NAME",
    "CLUSTER_NAME",
    "NUM_NODES",
    "VM_SIZE",
    "WORKER_CONTAINER_IMAGE",
    "SCHEDULER_CONTAINER_IMAGE"
  )
  
  lapply(expected_envs, function(e) {
    if (eval(parse(text=e)) == "") {
      stop("All variables in resource_spec.R must be set! Fill out resource_specs.R\
            and restart this script.")
    }
  })
  
  invisible(lapply(expected_envs, function(e) set_env(e, eval(parse(text=e)))))
  
}


replace_var <- function(var_name, json) {
  pattern <- paste0("\\{", var_name, "\\}")
  gsub(pattern, get_env(var_name), json)
}


replace_template_vars <- function(logic_app_json) {
  vars <- get_dotenv_vars()
  for (var in vars) {
    logic_app_json <- replace_var(var, logic_app_json)
  }
  logic_app_json
}