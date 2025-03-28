# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast

import boto3
from botocore.exceptions import ClientError

secrets_manager_client = boto3.client('secretsmanager')


def get_secret(secret_name):
    """
    シークレット取得
    Parameters
    ----------
    secret_name : string
        シークレット名

    Returns
    -------
    secret : dict
        シークレット値
    """
    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )
        secret = ast.literal_eval(get_secret_value_response['SecretString'])
        return secret
    except ClientError as e:
        raise e
