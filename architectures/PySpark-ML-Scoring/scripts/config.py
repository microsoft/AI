##------------------------------------------------------------------------------------------
## This scrip is used to customize the Databrick jobs script for the user's own
## Azure databricks instance.
##
## > python scripts/config.py --username <uname@example.com> --clusterID <cluster id> ./jobs/
##
## Where:
##       uname@example.com corresponds to the users Azure AD username
##       found in the Azure Databricks Workspace pathname.
##
##      clusterID denotes the Azure Databricks cluster to execute the job.
##      found from the databricks CLI command:
##
##      databricks clusters list
##
##
##​ Copyright (C) Microsoft Corporation. All rights reserved.​  ​
##------------------------------------------------------------------------------------------

import argparse
import os
import glob
import sys

def main():
    parser = argparse.ArgumentParser(
        description="searches the supplied folder for Databricks Jobs json template files (.tmpl),\n"
        + "and configures the scripts to connect to the Databricks with clusterID and username provided."
    )
    parser.add_argument(
        "-c",
        "--clusterID",
        type=str,
        help="The cluster ID is found using the databricks CLI command:\n"
        + "\ndatabricks clusters list\n",
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Found from the Databricks Workspace and should look like\n"
        + "your active directory email address.",
    )
    parser.add_argument(
        "template_dir",
        type=str,
        help="the directory containing the Databrick job json templates (./jobs/).",
    )

    args = parser.parse_args()

    for filename in glob.glob(os.path.join(args.template_dir, "*.tmpl")):
        with open(filename, "r") as f:
            s = f.read()
            if "<clusterid>" in s:
                s = s.replace("<clusterid>", args.clusterID)
            if "<uname@example.com>" in s:
                s = s.replace("<uname@example.com>", args.username)

        fname = filename.replace("tmpl", "json")
        with open(fname, "w") as fs:
            fs.write(s)
        print(filename)
        
if __name__ == "__main__":
    main()
