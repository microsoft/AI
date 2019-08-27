# Copyright (C) Microsoft Corporation.  All rights reserved.

from __future__ import print_function
import os
from azureml.core.authentication import (
    AzureCliAuthentication, InteractiveLoginAuthentication,
    ServicePrincipalAuthentication, AuthenticationException)

def get_auth():
    """Get an auth object for use with Workspace objects."""
    if os.environ.get("AML_SP_PASSWORD", None):
        print("Trying to create Workspace with Service Principal")
        aml_sp_password = os.environ.get("AML_SP_PASSWORD")
        aml_sp_tenant_id = os.environ.get("AML_SP_TENANT_ID")
        aml_sp_username = os.environ.get("AML_SP_USERNAME")
        auth = ServicePrincipalAuthentication(
            tenant_id=aml_sp_tenant_id,
            service_principal_id=aml_sp_username,
            service_principal_password=aml_sp_password
        )
    else:
        print("Trying to create Workspace with CLI Authentication")
        try:
            auth = AzureCliAuthentication()
            auth.get_authentication_header()
        except AuthenticationException:
            print("Trying to create Workspace with Interactive login")
            auth = InteractiveLoginAuthentication()
    return auth
