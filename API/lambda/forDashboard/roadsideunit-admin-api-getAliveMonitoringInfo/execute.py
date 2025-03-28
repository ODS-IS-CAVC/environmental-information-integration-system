# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging

import redis
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def get_data(redis_host):
    """
    死活監視情報取得
    Parameters
    ----------
    redis_host
        redis接続用ホスト

    Returns
    -------
    data : list
        取得データ
    response_status : int
        レスポンスステータス
    """
    data = []
    response_status = 200

    try:
        # 死活監視情報取得
        data = get_all_items(redis_host)

        if len(data) == 0:
            response_status = 204

    except Exception:
        logger.error('other error')
        raise

    return data, response_status


def get_all_items(redis_host):
    """
    ElastiCacheデータ全件取得
    Parameters
    ----------
    redis_host
       redis接続用ホスト

    Returns
    -------
    items : list
        取得データ
    """
    items = []

    # ElastiCacheに接続
    redis_client = redis.StrictRedis(
        host=redis_host,
        port='6379',
        decode_responses=True,
        db=1,
    )

    cursor = 0
    all_keys = []

    while True:
        # 1000件ごとにキー取得
        cursor, keys = redis_client.scan(cursor=cursor, count=1000)
        all_keys.extend(sorted(keys))
        if cursor == 0:
            break

    if len(all_keys) > 0:
        str_items = redis_client.mget(all_keys)
        items = list(map(lambda x: json.loads(x), str_items))

    return items
