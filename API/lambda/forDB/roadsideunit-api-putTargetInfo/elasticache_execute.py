import json
import logging

import redis
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def put_data(parameters, redis_host):
    """
    物標情報登録
    parameters
    ----------
    parameters : Array
        物標情報パラメータ
    redis_host
        redis接続用のホスト

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    try:
        # ElastiCacheに接続
        redis_client = redis.StrictRedis(
            host=redis_host,
            port='6379',
            decode_responses=True,
            db=0
        )

        # 機器情報数分だけループして登録
        for deviceIndividual in parameters['attribute']['deviceIndividualInfo']:
            # セットするキーを作成
            target_key = f"r{parameters['attribute']['roadsideUnitID']}s{parameters['attribute']['serviceLocationID']}d{deviceIndividual['deviceID']}"

            # セットする情報を再構築
            target_value = {
                'attribute': {
                    'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
                    'serviceLocationID': parameters['attribute']['serviceLocationID'],
                    'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
                    'formatVersion': parameters['attribute']['formatVersion'],
                    'deviceIndividualInfo': deviceIndividual
                }
            }
            if 'dataModelType' in parameters:
                target_value['dataModelType'] = parameters['dataModelType']

            target_value = json.dumps(target_value)

            # 物標情報登録
            redis_client.mset({target_key: target_value})

    except Exception:
        logger.error('other error')
        raise

    return response_status
