#!/usr/bin/python3
import argparse
from azure.keyvault import KeyVaultClient
from azure.common.client_factory import get_client_from_cli_profile
import os

def set_secret(kv_endpoint, secret_name, secret_value):
    client = get_client_from_cli_profile(KeyVaultClient)

    client.set_secret(kv_endpoint, secret_name, secret_value)
    return "Successfully created secret: {secret_name} in keyvault: {kv_endpoint}".format(secret_name=secret_name, kv_endpoint=kv_endpoint)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--secretName', required=True,
                        help="The name of the secret")

    return parser.parse_args()


if __name__ == "__main__":
       
    # hard coded for now
    kv_endpoint = "https://t3scriptkeyvault.vault.azure.net/"
    args = parse_args()
    key = os.getenv("storage_conn_string")
    message = set_secret(kv_endpoint, args.secretName, key)

    print(message)
