import re
import sys


MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"


def check_module(module_name):
    if not re.match(MODULE_REGEX, module_name):
        print(
            "ERROR: The project slug {} is not a valid Python module name. Please do not use a - and use _ instead".format(
                module_name
            )
        )

        # Exit to cancel project
        sys.exit(1)


def check_sub_id(sub_id):
    if len(sub_id) == 0:
        print(
            "ERROR: The subscription id is missing, please enter a valid subscription id slug"
        )

        # Exit to cancel project
        sys.exit(1)


def check_image_name(image_name):
    if "_" in image_name:
        print(
            "ERROR: The image name must not have underscores in it {}".format(
                image_name
            )
        )

        # Exit to cancel project
        sys.exit(1)


if __name__ == "__main__":
    check_module("{{cookiecutter.project_name}}")
    check_sub_id("{{cookiecutter.subscription_id}}")
    check_image_name("{{cookiecutter.image_name}}")
    print("All checks passed")
    if "{{ cookiecutter.deployment_type }}" == "aks":
        print("Creating AKS project...")

    if "{{ cookiecutter.deployment_type }}" == "iotedge":
        print("Creating IOT Edge project...")
