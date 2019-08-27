import pandas as pd
import re
import math
import gzip
import requests
import json
import ipywidgets as widgets
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core.authentication import AuthenticationException

from dotenv import set_key, get_key
import logging


def read_csv_gz(url, **kwargs):
    """Load raw data from a .tsv.gz file into Pandas data frame."""
    df = pd.read_csv(gzip.open(requests.get(url, stream=True).raw, mode='rb'),
                     sep='\t', encoding='utf8', **kwargs)
    return df.set_index('Id')


def clean_text(text):
    """Remove embedded code chunks, HTML tags and links/URLs."""
    if not isinstance(text, str):
        return text
    text = re.sub('<pre><code>.*?</code></pre>', '', text)
    text = re.sub('<a[^>]+>(.*)</a>', replace_link, text)
    return re.sub('<[^>]+>', '', text)


def replace_link(match):
    if re.match('[a-z]+://', match.group(1)):
        return ''
    else:
        return match.group(1)


def round_sample(X, frac=0.1, min=1):
    """Sample X ensuring at least min samples are selected."""
    n = max(min, math.floor(len(X) * frac))
    return X.sample(n)


def round_sample_strat(X, strat, **kwargs):
    """Sample X ensuring at least min samples are selected."""
    return X.groupby(strat).apply(round_sample, **kwargs)


def random_merge(A, B, N=20, on='AnswerId', key='key', n='n'):
    """Pair all rows of A with 1 matching row on "on" and N-1 random rows from B
    """
    assert key not in A and key not in B
    X = A.copy()
    X[key] = A[on]
    Y = B.copy()
    Y[key] = B[on]
    match = X.merge(Y, on=key).drop(key, axis=1)
    match[n] = 0
    df_list = [match]
    for i in A.index:
        X = A.loc[[i]]
        Y = B[B[on] != X[on].iloc[0]].sample(N-1)
        X[key] = 1
        Y[key] = 1
        Z = X.merge(Y, how='outer', on=key).drop(key, axis=1)
        Z[n] = range(1, N)
        df_list.append(Z)
    df = pd.concat(df_list, ignore_index=True)
    return df


def text_to_json(text):
    return json.dumps({'input': '{0}'.format(text)})


def write_json_to_file(json_dict, filename, mode='w'):
    with open(filename, mode) as outfile:
        json.dump(json_dict, outfile, indent=4, sort_keys=True)
        outfile.write('\n\n')


def read_questions(path, id, answerid):
    """Read in a questions file with at least Id and AnswerId columns."""
    questions = pd.read_csv(path, sep='\t', encoding='latin1')
    questions[id] = questions[id].astype(str)
    questions[answerid] = questions[answerid].astype(str)
    questions = questions.set_index(id, drop=False)
    questions.sort_index(inplace=True)
    return questions

def get_auth(env_path):
    logger = logging.getLogger(__name__)
    if get_key(env_path, 'password') != "YOUR_SERVICE_PRINCIPAL_PASSWORD":
        logger.debug("Trying to create Workspace with Service Principal")
        aml_sp_password = get_key(env_path, 'password')
        aml_sp_tennant_id = get_key(env_path, 'tenant_id')
        aml_sp_username = get_key(env_path, 'username')
        auth = ServicePrincipalAuthentication(
            tenant_id=aml_sp_tennant_id,
            username=aml_sp_username,
            password=aml_sp_password
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
