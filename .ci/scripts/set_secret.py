#!/usr/bin/python3

import argparse
from azure.keyvault import KeyVaultClient
from azure.common.client_factory import get_client_from_cli_profile


def set_secret(kv_endpoint, secret_name, secret_value):
    client = get_client_from_cli_profile(KeyVaultClient)
    client.set_secret(kv_endpoint, secret_name, secret_value)


if __name__ == "__main__":
    # hard coded for now
    kv_endpoint = "https://t3scriptkeyvault.vault.azure.net/"
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--secretName', required=True,
                        help="The name of the secret")
    parser.add_argument('-v', '--secretValue', required=True,
                        help="The value of the secret")

    args = parser.parse_args()

    set_secret(kv_endpoint, args.secretName, args.secretValue)
