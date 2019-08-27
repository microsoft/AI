# Create a batch scoring Databricks Job

The batch scoring process is actually a pipeline of operations. We assume raw data arrives through the some process. The scoring operation has to transform the raw data into the correct format for the model to consume, then the model makes predictions which we store for later consumption. 

We've created the `notebooks/3_Scoring_Pipeline.ipynb` to execute a full scoring pipeline. The notebook takes a `start_date` and `to_date`, as well as a `model` to indicate which model to use and a `results_table` name to store the model predictions. The notebook runs the `notebooks/2a_feature_engineering.ipynb` notebook to transform the data, storing the scoring data in a temporary table and then runs the `notebooks/3a_model_scoring.ipynb` notebook with the specified model and results data target data set to store the model predictions. 

## Customize the JSON templates

You can create Databricks jobs through the Azure Databricks workspace portal or through the Databricks CLI. We demonstrate using the CLI and have provided a set of Job template files. Before using these templates, you will need to provide the information to connect to your specific Databricks instance. 

1. The Databricks Cluster ID you want to run the job on.

You can find the ClusterID by navigating to the Clusters pane in the Azure Databricks workspace portal. Click on Advanced Options and the ClusterID is listed under the Tags tab. You can also get the ClusterID using the Databricks CLI. Assuming you have already connected the CLI to your Databricks instance, run the following command from a terminal window to get **the cluster ID from the first field** of the resulting table. It is important to use the clusterID, not the cluster name, for the job to execute.

```
databricks clusters list
```

2. The workspace username containing the notebooks to run.

This will be the same username you used to copy the notebooks to your workspace and should take the form of `username@example.com`.

Using this information, we have provided a script to customize the templates for connecting to your Databricks cluster. Execute the following command from a terminal window, in your repository root directory.

```
python scripts/config.py  -c <clusterID> -u <username@example.com> ./jobs/
```

This command reads the `./jobs/*.tmpl` files, replaces the clusterID and username placeholder strings with the specifics for your Databricks cluster, storing the modified files to the JSON jobs scripts we'll use to setup and demonstrate the Batch scoring processes.


## Create the batch scoring job

Create the scoring pipeline job using the CLI command:

`databricks jobs create --json-file jobs/3_CreateScoringPipeline.json`

This particular batch job is configured to only run on demand as our example data does not change with time. Using the `<jobID>` returned from the create command, run the job manually with default parameters specified in the scoring notebook with the following command.

`databricks jobs run-now --job-id <jobID>`

To specify different notebook input parameters, use the following call on Windows (we need to escape out the quote characters).
```
databricks jobs run-now --job-id <jobID> --notebook-params {\"start_date\":\"2015-11-15\",\"to_date\":\"2017-01-01\",\"results_data\":\"predictions\",\"model\":\"RandomForest\"}
```

**note** We have noticed issues running this on Mac OS X. We should be able to use this command, 
```
databricks jobs run-now --job-id <jobID> --notebook-params {"results_data":"predictions","model":"RandomForest","start_date":"2015-11-15","to_date":"2017-01-01"}
```
However this seems to fail consistently. This is a known Databricks CLI issue. 

The entire workflow job will take about 2-3 minutes to complete given this 2.5 months of data.

## Further customization

For our example, we only run the batch scoring job on demand. This keeps your costs down, since the example data does not change with time. 

In a real scenario, we would expect the data ingestion step to be automated. As data arrives on the datastore, we could then periodically run the batch scoring job automatically. You can customize the `jobs/3_CreateScoringPipeline.json` (or .tmpl) files in your local repository to run the Azure Databricks job on a schedule by adding the following code block below the `"notebook_tasks":` block.

```
"schedule": {
    "quartz_cron_expression": "0 30 7-18 ? * *",
    "timezone_id": "America/Los_Angeles"
  },
```

The `quartz_cron_expression` takes [Quartz cron](http://www.quartz-scheduler.org/documentation/quartz-2.1.x/tutorials/tutorial-lesson-06.html) style arguments. In this example, the job will run every hour on the half hour, between 7:30am and 6:30pm every day. More details to customize this scheduler can be found in the documentation at (https://docs.databricks.com/api/latest/jobs.html#jobscronschedule)

# Conclusion

The actual work of this scenario is done through this Azure Databricks job. The job executes the `3_Scoring_Pipeline` notebook, which depends on a machine learning model existing on the Azure Databricks file storage. We created the model using the `2_Training_Pipeline` notebook which used the data downloaded with the `1_data_ingestion` notebook.
