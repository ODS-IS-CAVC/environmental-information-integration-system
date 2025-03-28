# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
SIGNAL_INFO_TABLE_NAME = os.environ['SIGNAL_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_signal_info = dynamoDB.Table(SIGNAL_INFO_TABLE_NAME)


def get_data():
    """
    信号情報全件取得
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
        # 信号情報全件取得
        data_list, response_status = get_data_execute(response_status)
    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(response_status):
    """
    信号情報全件取得
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

    # 信号情報全件取得
    response = t_signal_info.scan()

    signal_items = response['Items']

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループする
    while 'LastEvaluatedKey' in response:
        response = t_signal_info.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        signal_items.extend(response['Items'])

    # 信号情報取得できた場合
    if len(signal_items) != 0:
        # 結果を代入
        for signal_item in signal_items:
            temporary_result = {}
            if 'dataModelType' in signal_item:
                temporary_result['dataModelType'] = str(signal_item.get('dataModelType'))
            temporary_result['attribute'] = {}
            temporary_result['attribute']['serviceLocationID'] = int(signal_item.get('serviceLocationID'))
            temporary_result['attribute']['roadsideUnitID'] = int(signal_item.get('roadsideUnitID'))
            temporary_result['attribute']['updateTimeInfo'] = str(signal_item.get('updateTimeInfo'))
            temporary_result['attribute']['formatVersion'] = int(signal_item.get('formatVersion'))
            temporary_result['attribute']['prefectureID'] = int(signal_item.get('prefectureID'))
            temporary_result['attribute']['roadType'] = int(signal_item.get('roadType'))
            temporary_result['attribute']['intersectionID'] = int(signal_item.get('intersectionID'))
            result.append(temporary_result)
    else:
        response_status = 204
    return result, response_status
