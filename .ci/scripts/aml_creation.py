#!/usr/bin/python

import azureml.core
from azureml.core import Workspace
from dotenv import set_key, get_key, find_dotenv
from pathlib import Path
from AIHelpers.utilities import get_auth

import sys, getopt

def main(argv):  
  try:
     opts, args = getopt.getopt(argv,"hs:rg:wn:wr:",["subscription_id=","resource_group=","workspace_name=", "workspace_region="])
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

if __name__ == "__main__":
  print("AML SDK Version:", azureml.core.VERSION)
  main(sys.argv[1:])
  
  # Azure resources
  subscription_id = "{{cookiecutter.subscription_id}}"
  resource_group = "{{cookiecutter.resource_group}}"  
  workspace_name = "{{cookiecutter.workspace_name}}"  
  workspace_region = "{{cookiecutter.workspace_region}}"
