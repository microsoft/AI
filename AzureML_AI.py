import azureml.core
from azureml.core import Workspace
from dotenv import set_key, get_key, find_dotenv
from pathlib import Path
from AIHelpers.utilities import get_auth, AIErrorPredictor, AzureRegionRecommender
import sys, getopt
import logging

# Configure logging
logging.basicConfig(filename='aml_creation.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def validate_input(subscription_id, resource_group, workspace_name, workspace_region):
    # AI-driven validation of inputs
    if not subscription_id:
        logging.error("Subscription ID is missing")
        raise ValueError("Subscription ID is required")
    if not resource_group:
        logging.error("Resource Group is missing")
        raise ValueError("Resource Group is required")
    if not workspace_name:
        logging.error("Workspace Name is missing")
        raise ValueError("Workspace Name is required")
    if not workspace_region:
        logging.warning("Workspace Region is missing. Suggesting optimal region...")
        workspace_region = AzureRegionRecommender.recommend_region(subscription_id)
        logging.info(f"Suggested region: {workspace_region}")
    return workspace_region

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:rg:wn:wr:", ["subscription_id=", "resource_group=", "workspace_name=", "workspace_region="])
    except getopt.GetoptError:
        print('aml_creation.py -s <subscription_id> -rg <resource_group> -wn <workspace_name> -wr <workspace_region>')
        sys.exit(2)

    subscription_id, resource_group, workspace_name, workspace_region = None, None, None, None

    for opt, arg in opts:
        if opt == '-h':
            print('aml_creation.py -s <subscription_id> -rg <resource_group> -wn <workspace_name> -wr <workspace_region>')
            sys.exit()
        elif opt in ("-s", "--subscription_id"):
            subscription_id = arg
        elif opt in ("-rg", "--resource_group"):
            resource_group = arg
        elif opt in ("-wn", "--workspace_name"):
            workspace_name = arg
        elif opt in ("-wr", "--workspace_region"):
            workspace_region = arg

    try:
        workspace_region = validate_input(subscription_id, resource_group, workspace_name, workspace_region)
        env_path = find_dotenv()
        if env_path == "":
            Path(".env").touch()
            env_path = find_dotenv()

        # AI-driven error prediction
        if AIErrorPredictor.predict_error(subscription_id, resource_group, workspace_name):
            logging.warning("Potential error detected. Proceeding with caution...")

        ws = Workspace.create(
            name=workspace_name,
            subscription_id=subscription_id,
            resource_group=resource_group,
            location=workspace_region,
            create_resource_group=True,
            auth=get_auth(env_path),
            exist_ok=True,
        )
        logging.info("Workspace created successfully")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("AML SDK Version:", azureml.core.VERSION)
    main(sys.argv[1:])

    # Azure resources for templating
    subscription_id = "{{cookiecutter.subscription_id}}"
    resource_group = "{{cookiecutter.resource_group}}"
    workspace_name = "{{cookiecutter.workspace_name}}"
    workspace_region = "{{cookiecutter.workspace_region}}"
