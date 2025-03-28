# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
from datetime import datetime

import redis
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def get_data(roadside_unit_id, service_location_id, query_params, redis_host):
    """
    物標情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    query_params : list
        クエリパラメータ
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
        # 物標情報取得
        data_list, response_status = get_data_execute(roadside_unit_id, service_location_id, query_params, redis_host, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(roadside_unit_id, service_location_id, query_params, redis_host, response_status):
    """
    物標情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    query_params : list
        クエリパラメータ
    redis_host
       redis接続用のホスト
    response_status : int
        処理完了ステータス

    Returns
    -------
    result : Array
        取得されたデータ
    """

    result = []
    target_key_name = ''

    # ElastiCacheに接続
    redis_client = redis.StrictRedis(
        host=redis_host,
        port='6379',
        decode_responses=True,
        db=0
    )

    # クエリパラメータにdeviceIDが存在している場合
    if 'deviceID' in query_params:
        device_id = query_params['deviceID']

        # 検索するキーの名前を定義
        target_key_name = f'r{roadside_unit_id}s{service_location_id}d{device_id}'

        # ElastiCache内からデータを取得
        target_items = get_elasticache_items(redis_client, target_key_name)

    # クエリパラメータにdeviceIDが存在していない場合
    else:
        # 検索するキーの名前を定義
        target_key_name = f'r{roadside_unit_id}s{service_location_id}d*'

        # ElastiCache内を全件検索し合致するキーを抽出
        target_items = get_elasticache_items(redis_client, target_key_name)

    # 物標情報を整形し、取得
    result, response_status = get_target_value(target_items, response_status)

    return result, response_status


def get_elasticache_items(redis_client, target_key_name):
    """
    キーを全件検索し、ElastiCacheからデータを取得
    Parameters
    ----------
    redis_client :
        接続したElastiCache
    target_key_name : string
        物標キー名

    Returns
    -------
    all_items : Array
        検索したデータ
    """
    cursor = 0
    all_keys = []

    while True:
        # 1000件ごとに全件検索
        cursor, keys = redis_client.scan(cursor=cursor, match=target_key_name, count=1000)
        all_keys.extend(sorted(keys))
        if cursor == 0:
            break

    all_items = redis_client.mget(all_keys)

    return all_items


def get_target_value(target_items, response_status):
    """
    物標情報を整形し、取得
    Parameters
    ----------
    target_items : Array
        物標データ
    response_status : int
        処理完了ステータス

    Returns
    -------
    result : dict
        取得されたデータ
    response_status : int
        処理完了ステータス
    """

    result = {}
    latest_update_time = ''
    is_first = True

    if len(target_items) != 0:
        for target_item in target_items:
            target_item = json.loads(target_item)

            # 最初のループのみdeviceIndividualInfo以外の項目を代入
            if is_first is True:
                if 'dataModelType' in target_item:
                    result['dataModelType'] = str(target_item['dataModelType'])
                result['attribute'] = {}
                result['attribute']['serviceLocationID'] = int(target_item['attribute']['serviceLocationID'])
                result['attribute']['roadsideUnitID'] = int(target_item['attribute']['roadsideUnitID'])
                result['attribute']['updateTimeInfo'] = ''
                result['attribute']['formatVersion'] = int(target_item['attribute']['formatVersion'])
                result['attribute']['deviceNum'] = 0
                result['attribute']['deviceIndividualInfo'] = []
                is_first = False

            # updateTimeInfo比較し、変数に値がない場合代入
            if latest_update_time == '':
                latest_update_time = datetime.strptime(target_item['attribute']['updateTimeInfo'], '%Y-%m-%dT%H:%M:%S.%f%z')
                result['attribute']['updateTimeInfo'] = target_item['attribute']['updateTimeInfo']
            # updateTimeInfoを比較し、最新のupdateTimeInfoを代入
            else:
                current_update_time = datetime.strptime(target_item['attribute']['updateTimeInfo'], '%Y-%m-%dT%H:%M:%S.%f%z')
                if current_update_time > latest_update_time:
                    latest_update_time = current_update_time
                    result['attribute']['updateTimeInfo'] = target_item['attribute']['updateTimeInfo']

            # すべてのループでdeviceIndividualInfoを代入
            result['attribute']['deviceIndividualInfo'].append(target_item['attribute']['deviceIndividualInfo'])

        result['attribute']['deviceNum'] = len(result['attribute']['deviceIndividualInfo'])

    else:
        response_status = 204
    return result, response_status
