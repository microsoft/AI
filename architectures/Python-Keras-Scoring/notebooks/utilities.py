from azureml.core.authentication import (AuthenticationException,
                                         AzureCliAuthentication,
                                         InteractiveLoginAuthentication,
                                         ServicePrincipalAuthentication)
import logging
import os


def get_auth():
    logger = logging.getLogger(__name__)
    if os.environ.get("AML_SP_PASSWORD", None):
        logger.debug("Trying to create Workspace with Service Principal")
        aml_sp_password = os.environ.get("AML_SP_PASSWORD")
        aml_sp_tennant_id = os.environ.get("AML_SP_TENNANT_ID")
        aml_sp_username = os.environ.get("AML_SP_USERNAME")
        auth = ServicePrincipalAuthentication(
            tenant_id=aml_sp_tennant_id,
            username=aml_sp_username,
            password=aml_sp_password,
        )
    else:
        logger.debug("Trying to create Workspace with CLI Authentication")
        try:
            auth = AzureCliAuthentication()
            auth.get_authentication_header()
        except AuthenticationException:
            logger.debug("Trying to create Workspace with Interactive login")
            auth = InteractiveLoginAuthentication()

    return auth
