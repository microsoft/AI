import json
import os
from dotenv import dotenv_values, set_key, find_dotenv, get_key
from getpass import getpass


def _create_env(dotenv_path):
    with open(dotenv_path, 'a'):
        os.utime(dotenv_path)


def dotenv_for():
    dotenv_path = find_dotenv()
    if dotenv_path == '':
        dotenv_path = '.env'
        _create_env(dotenv_path)
    return dotenv_path


def get_password(dotenv_path):
    if 'PASSWORD' not in dotenv_values(dotenv_path=dotenv_path):
        print('Password not set')
        password = getpass('Please enter password to use for the cluster')
        _ = set_key(dotenv_path, 'PASSWORD', password)
    return get_key(dotenv_path, 'PASSWORD')


def write_json_to_file(json_dict, filename, mode='w'):
    with open(filename, mode) as outfile:
        json.dump(json_dict, outfile, indent=4, sort_keys=True)
        outfile.write('\n\n')
