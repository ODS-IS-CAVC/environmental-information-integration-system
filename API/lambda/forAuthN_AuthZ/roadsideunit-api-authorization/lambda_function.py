# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os
import re
import traceback

import auth
import secret
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

API_SECRET_NAME = os.environ['API_SECRET_NAME']
SYSTEMAUTH_TOKEN_API_URL = os.environ['SYSTEMAUTH_TOKEN_API_URL']


def lambda_handler(event, context):
    """
    認可
    Parameters
    ----------
    event : dict
        イベント
    context :LambdaContext
        コンテキストオブジェクト

    Returns
    -------
    response :
        IAM ポリシー
    """
    try:
        logger.info(f"methodArn:{event['methodArn']}")
        response = {}

        headers = dict()
        for k, v in event['headers'].items():
            headers[k.lower()] = v

        authorization = headers['authorization']
        api_key = headers['apikey']

        # Authorizationヘッダー値にBearerがついているかチェック
        regex = r'^Bearer '
        if re.match(regex, authorization) is None:
            logger.error('Invalid access token')
            logger.error(f'Authorization: {authorization}')
            response = generate_policy('Deny', event['methodArn'])
            return response

        authorization = re.sub(regex, '', authorization)

        # シークレット取得
        api_secret = secret.get_secret(API_SECRET_NAME)

        # トークンイントロスペクションAPIを実行
        result = auth.token_introspection(
            SYSTEMAUTH_TOKEN_API_URL,
            api_secret['dataDistribution_apiKey'],
            authorization
        )
        if result:
            response = generate_policy('Allow', event['methodArn'], api_key)
        else:
            logger.error('Token introspection failed')
            logger.error(f'apiKey: {api_key}')
            logger.error(f'Authorization: {authorization}')
            response = generate_policy('Deny', event['methodArn'])
        return response

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())


def generate_policy(effect, resource, api_key=None):
    """
    ポリシー生成
    Parameters
    ----------
    effect : string
        認可判定
    resource : string
        ARN
    api_key : string
        APIキー

    Returns
    -------
    response :
        IAM ポリシー
    """
    policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
    if (api_key is not None):
        policy['usageIdentifierKey'] = api_key

    return policy
