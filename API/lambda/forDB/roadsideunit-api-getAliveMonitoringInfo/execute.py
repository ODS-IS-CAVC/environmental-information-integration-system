# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging

import redis
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def get_data(roadside_unit_id, service_location_id, redis_host):
    """
    死活監視情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    redis_host
        redis接続用のホスト

    Returns
    -------
    data_list : Array
        データ返却用配列
    response_status : int
        処理完了ステータス
    """

    data_list = []
    response_status = 200

    try:
        # 死活監視情報取得
        data_list, response_status = get_data_execute(roadside_unit_id, service_location_id, redis_host, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(roadside_unit_id, service_location_id, redis_host, response_status):
    """
    死活監視情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    redis_host
       redis接続用のホスト
    response_status : int
        処理完了ステータス

    Returns
    -------
    result : dict
        取得されたデータ
    response_status : int
        処理完了ステータス
    """

    # ElastiCacheに接続
    redis_client = redis.StrictRedis(
        host=redis_host,
        port='6379',
        decode_responses=True,
        db=1
    )

    # 検索するキーの名前を定義
    alive_monitoring_key = f'r{roadside_unit_id}s{service_location_id}'

    # ElastiCache内からデータを取得
    alive_monitoring_item = redis_client.get(alive_monitoring_key)

    result = {}
    if alive_monitoring_item is not None:
        alive_monitoring_item = json.loads(alive_monitoring_item)
        if 'dataModelType' in alive_monitoring_item:
            result['dataModelType'] = str(alive_monitoring_item['dataModelType'])
        result['attribute'] = {}
        result['attribute']['serviceLocationID'] = int(alive_monitoring_item['attribute']['serviceLocationID'])
        result['attribute']['roadsideUnitID'] = int(alive_monitoring_item['attribute']['roadsideUnitID'])
        result['attribute']['updateTimeInfo'] = str(alive_monitoring_item['attribute']['updateTimeInfo'])
        result['attribute']['formatVersion'] = int(alive_monitoring_item['attribute']['formatVersion'])
        result['attribute']['operationClassificationCode'] = int(alive_monitoring_item['attribute']['operationClassificationCode'])
        result['attribute']['serviceAvailability'] = int(alive_monitoring_item['attribute']['serviceAvailability'])
        result['attribute']['deviceClassificationNum'] = int(alive_monitoring_item['attribute']['deviceClassificationNum'])
        result['attribute']['deviceClassificationAliveInfo'] = alive_monitoring_item['attribute']['deviceClassificationAliveInfo']

    else:
        response_status = 204

    return result, response_status
