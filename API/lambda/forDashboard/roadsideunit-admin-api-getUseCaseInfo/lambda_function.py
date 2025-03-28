# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
import traceback
from decimal import Decimal

import execute
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    ユースケース情報の全件取得
    Returns
    -------
    response : json
        取得データ
    """

    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': ''
    }

    try:
        # データ取得
        data, res = execute.get_data()
        # データが存在している場合
        if res == 200:
            response['body'] = json.dumps(data, default=decimal_to_int)
        # データが存在しない場合
        elif res == 204:
            response['statusCode'] = res
            logger.info('Null data')

    except Exception:
        response['statusCode'] = 500
        response['body'] = 'Internal server error'
        logger.error('error roadsideunit-admin-api-getUseCaseInfo')
        logger.error(traceback.format_exc())

    return response


def decimal_to_int(obj):
    """
    decimalをintに変換
    Parameters
    ----------
    obj : decimal
        decimal値

    Returns
    -------
    response : int
        変換データ
    """
    if isinstance(obj, Decimal):
        return int(obj)
