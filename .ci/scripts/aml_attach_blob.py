#!/usr/bin/python

import azureml.core
from azureml.core import Workspace
from dotenv import set_key, get_key, find_dotenv
from pathlib import Path
from AIHelpers.utilities import get_auth

import sys, getopt

def main(argv):  
  try:
     opts, args = getopt.getopt(argv,"hs:rg:wn:wr:dsn:cn:an:ak:drg:",
      ["subscription_id=","resource_group=","workspace_name=", "workspace_region=","blob_datastore_name=","container_name=","account_name=","account_key=","datastore_rg="])
  except getopt.GetoptError:
     print 'aml_creation.py -s <subscription_id> -rg <resource_group> -wn <workspace_name> -wr <workspace_region>'
     sys.exit(2)
  for opt, arg in opts:
     if opt == '-h':
        print 'aml_creation.py -s <subscription_id> -rg <resource_group> -wn <workspace_name> -wr <workspace_region>'
        sys.exit()
     elif opt in ("-s", "--subscription_id"):
        subscription_id = arg
     elif opt in ("-rg", "--resource_group"):
        resource_group = arg
     elif opt in ("-wn", "--workspace_name"):
        workspace_name = arg
     elif opt in ("-wr", "--workspace_region"):
        workspace_region = arg
     elif opt in ("-dsn", "--blob_datastore_name"):
        workspace_region = arg
     elif opt in ("-cn", "--container_name"):
        workspace_region = arg
     elif opt in ("-an", "--account_name"):
        workspace_region = arg
     elif opt in ("-ak", "--account_key"):
        workspace_region = arg
     elif opt in ("-drg", "--datastore_rg"):
        workspace_region = arg
        
    env_path = find_dotenv()
    if env_path == "":
        Path(".env").touch()
        env_path = find_dotenv()

    ws = Workspace.create(
      name=workspace_name,
      subscription_id=subscription_id,
      resource_group=resource_group,
      location=workspace_region,
      create_resource_group=True,
      auth=get_auth(env_path),
      exist_ok=True,
    )
    blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=blob_datastore_name, 
                                                         container_name=container_name, 
                                                         account_name=account_name,
                                                         account_key=account_key,
                                                         resource_group=datastore_rg)

if __name__ == "__main__":
  print("AML SDK Version:", azureml.core.VERSION)
  main(sys.argv[1:])
