# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
COMMUNICATION_MEDIA_INFO_TABLE_NAME = os.environ['COMMUNICATION_MEDIA_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_communication_media_info = dynamoDB.Table(COMMUNICATION_MEDIA_INFO_TABLE_NAME)


def get_data():
    """
    通信メディア情報全件取得
    Returns
    -------
    data_list : array
        データ返却用配列
    response_status : int
        処理完了ステータス
    """

    data_list = []
    response_status = 200

    try:
        # 通信メディア情報全件取得
        data_list, response_status = get_data_execute(response_status)
    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(response_status):
    """
    通信メディア情報全件取得
    Parameters
    ----------
    response_status : int
        処理完了ステータス

    Returns
    -------
    result : array
        取得されたデータ
    response_status : int
        処理完了ステータス
    """

    result = []

    # 通信メディア情報全件取得
    response = t_communication_media_info.scan()

    communication_media_items = response['Items']

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループする
    while 'LastEvaluatedKey' in response:
        response = t_communication_media_info.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        communication_media_items.extend(response['Items'])

    # 通信メディア情報取得できた場合
    if len(communication_media_items) != 0:
        # 結果を代入
        for communication_media_item in communication_media_items:
            temporary_result = {}
            if 'dataModelType' in communication_media_item:
                temporary_result['dataModelType'] = str(communication_media_item.get('dataModelType'))
            temporary_result['attribute'] = {}
            temporary_result['attribute']['serviceLocationID'] = int(communication_media_item.get('serviceLocationID'))
            temporary_result['attribute']['roadsideUnitID'] = int(communication_media_item.get('roadsideUnitID'))
            temporary_result['attribute']['updateTimeInfo'] = str(communication_media_item.get('updateTimeInfo'))
            temporary_result['attribute']['formatVersion'] = int(communication_media_item.get('formatVersion'))
            temporary_result['attribute']['communicationMediaNum'] = int(communication_media_item.get('communicationMediaNum'))
            temporary_result['attribute']['communicationMediaIDs'] = ast.literal_eval(communication_media_item.get('communicationMediaIDs'))
            result.append(temporary_result)
    else:
        response_status = 204
    return result, response_status
