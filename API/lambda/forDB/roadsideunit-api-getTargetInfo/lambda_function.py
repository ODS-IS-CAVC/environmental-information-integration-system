# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
import os
import traceback
from decimal import Decimal

import dynamodb_execute
import elasticache_execute
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
REDIS_HOST = os.environ['REDIS_HOST']


def lambda_handler(event, context):
    """
    物標情報の取得
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
        headers = dict()
        for k, v in event['headers'].items():
            headers[k.lower()] = v
        if 'x-tracking' in headers:
            logger.info(headers['x-tracking'])

        # パラメータ取得
        roadside_unit_id = event['queryStringParameters']['roadsideUnitID']
        service_location_id = event['queryStringParameters']['serviceLocationID']

        query_params = event.get('queryStringParameters', {})

        # パラメータにて時間の指定がされている場合はDynamoDBからデータを取得
        if 'startAt' in query_params or 'endAt' in query_params:
            # DynamoDBからデータ取得
            data, res = dynamodb_execute.get_data(roadside_unit_id, service_location_id, query_params)
        # パラメータの時間指定がない場合はElastiCacheから最新のデータを取得
        else:
            # ElastiCacheからデータ取得
            data, res = elasticache_execute.get_data(roadside_unit_id, service_location_id, query_params, REDIS_HOST)

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
        logger.error('error roadsideunit-api-getTargetInfo')
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
