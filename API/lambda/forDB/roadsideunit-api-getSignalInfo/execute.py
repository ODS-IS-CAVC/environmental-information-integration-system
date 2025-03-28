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


def get_data(service_location_id, roadside_unit_id):
    """
    信号情報取得
    Parameters
    ----------
    service_location_id : int
        サービス地点情報
    roadside_unit_id : int
        路側機ID

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
        # 信号情報取得
        data_list, response_status = get_data_execute(service_location_id, roadside_unit_id, response_status)

    except Exception:
        logger.error('other data')
        raise

    return data_list, response_status


def get_data_execute(service_location_id, roadside_unit_id, response_status):
    """
    信号情報取得
    Parameters
    ----------
    service_location_id : int
        サービス地点情報ID
    roadside_unit_id : int
        路側機ID
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

    # 信号情報取得
    signal_item = t_signal_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(int(roadside_unit_id)) & Key('serviceLocationID').eq(int(service_location_id))
    )

    # 信号情報取得できた場合
    if signal_item['Items']:
        # 結果を代入
        signal_item = signal_item['Items'][0]

        if 'dataModelType' in signal_item:
            result['dataModelType'] = str(signal_item.get('dataModelType'))
        result['attribute'] = {}
        result['attribute']['serviceLocationID'] = int(signal_item.get('serviceLocationID'))
        result['attribute']['roadsideUnitID'] = int(signal_item.get('roadsideUnitID'))
        result['attribute']['updateTimeInfo'] = str(signal_item.get('updateTimeInfo'))
        result['attribute']['formatVersion'] = int(signal_item.get('formatVersion'))
        result['attribute']['prefectureID'] = int(signal_item.get('prefectureID'))
        result['attribute']['roadType'] = int(signal_item.get('roadType'))
        result['attribute']['intersectionID'] = int(signal_item.get('intersectionID'))

    else:
        response_status = 204

    return result, response_status
