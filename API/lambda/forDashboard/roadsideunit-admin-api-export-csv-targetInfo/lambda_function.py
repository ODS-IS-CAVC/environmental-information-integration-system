# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
import os
import traceback

from log import logger

import execute

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
TARGET_INFO_TABLE_NAME = os.environ['TARGET_INFO_TABLE_NAME']
SENSOR_INFO_TABLE_NAME = os.environ['SENSOR_INFO_TABLE_NAME']
TARGET_INFO_BUCKET_NAME = os.environ['TARGET_INFO_BUCKET_NAME']
REGION_NAME = os.environ['REGION_NAME']


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
        'body': ''
    }

    try:
        # パラメータ取得
        query_params = event.get('queryStringParameters', {})

        # パラメータチェック
        # 期間指定が10分(600秒)を超える場合
        if int(query_params['period']) > 600:
            response['statusCode'] = 400
            logger.error('Outside period')
            return response

        # 期間指定が1秒を下回る場合
        if int(query_params['period']) < 1:
            response['statusCode'] = 400
            logger.error('Outside period')
            return response

        # DynamoDBからデータを取得
        data, res = execute.get_data(query_params, TARGET_INFO_TABLE_NAME, SENSOR_INFO_TABLE_NAME)

        # データが存在しない場合
        if res == 204:
            response['statusCode'] = res
            logger.info('No Content')
            return response

        # データを整形し、csv出力
        result = execute.data_format(data, query_params, TARGET_INFO_BUCKET_NAME, TARGET_INFO_TABLE_NAME, REGION_NAME)

        # s3バケットのパスをbodyに返す
        response['body'] = json.dumps(result)

    except Exception:
        response['statusCode'] = 500
        response['body'] = 'Internal server error'
        logger.error('error roadsideunit-api-getTargetInfo')
        logger.error(traceback.format_exc())

    return response
