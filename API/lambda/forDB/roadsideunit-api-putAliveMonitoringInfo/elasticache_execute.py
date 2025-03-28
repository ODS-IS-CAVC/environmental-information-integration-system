# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging

import redis
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def put_data(parameters, redis_host):
    """
    死活監視情報登録
    parameters
    ----------
    parameters : Array
        死活監視情報パラメータ
    redis_host
        redis接続用のホスト

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    try:
        # ElasticCacheに接続
        redis_client = redis.StrictRedis(
            host=redis_host,
            port='6379',
            decode_responses=True,
            db=1
        )

        # セットするキーを作成
        alive_monitoring_key = f"r{parameters['attribute']['roadsideUnitID']}s{parameters['attribute']['serviceLocationID']}"

        # セットする情報を再構築
        alive_monitoring_value = {
            'attribute': {
                'serviceLocationID': parameters['attribute']['serviceLocationID'],
                'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
                'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
                'formatVersion': parameters['attribute']['formatVersion'],
                'operationClassificationCode': parameters['attribute']['operationClassificationCode'],
                'serviceAvailability': parameters['attribute']['serviceAvailability'],
                'deviceClassificationNum': parameters['attribute']['deviceClassificationNum'],
                'deviceClassificationAliveInfo': parameters['attribute']['deviceClassificationAliveInfo']
            }
        }
        if 'dataModelType' in parameters:
            alive_monitoring_value['dataModelType'] = parameters['dataModelType']

        alive_monitoring_value = json.dumps(alive_monitoring_value)

        # 死活監視情報登録
        redis_client.mset({alive_monitoring_key: alive_monitoring_value})

    except Exception:
        logger.error('other error')
        raise

    return response_status
