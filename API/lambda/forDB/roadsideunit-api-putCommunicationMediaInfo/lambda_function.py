# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
import traceback

import execute
import get_parameter
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    通信メディア情報作成
    Returns
    -------
    response : json
        取得データ
    """

    # レスポンス定義
    response = {
        'statusCode': 200,
        'body': ''
    }

    # リクエスト定義
    request = {
        'body': ''
    }

    try:
        # curlの場合
        if type(event['body']) is dict:
            request['body'] = json.dumps(event['body'], default=str)
        # Postmanから実行の場合
        else:
            request['body'] = \
                event['body'].replace('\\n', '').replace('\\r', '')

        headers = dict()
        for k, v in event['headers'].items():
            headers[k.lower()] = v
        if 'x-tracking' in headers:
            logger.info(headers['x-tracking'])

        # パラメータ取得
        parameters = get_parameter.get_body(request['body'])

        # データ判別フラグ取得
        data_exists_flag = execute.get_data(
            parameters['attribute']['roadsideUnitID'],
            parameters['attribute']['serviceLocationID']
        )

        # 通信メディア情報登録更新処理
        res = execute.put_data(parameters, data_exists_flag)

        # 通信メディア情報更新の場合は受け取ったデータを返す
        if res == 200:
            response['body'] = json.dumps(parameters)

        response['statusCode'] = res

    except Exception:
        response['statusCode'] = 500
        response['body'] = 'Internal server error'
        logger.error('error roadsideunit-api-putCommunicationMediaInfo')
        logger.error(traceback.format_exc())

    return response
