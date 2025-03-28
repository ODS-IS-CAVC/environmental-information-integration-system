# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import logging
import os

import boto3
from botocore.exceptions import ClientError
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
SIGNAL_INFO_TABLE_NAME = os.environ['SIGNAL_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key


def get_data(service_location_id, roadside_unit_id):
    """
    センサ情報取得
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
        # センサ情報取得
        data_list, response_status = get_data_execute(service_location_id, roadside_unit_id, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(service_location_id, roadside_unit_id, response_status):
    """
    センサ情報取得
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

    # 取得するセンサ情報テーブル名を作成
    base_table_name = SIGNAL_INFO_TABLE_NAME
    t_sensor_name = f"{base_table_name}_{roadside_unit_id}"

    t_sensor_info = dynamoDB.Table(t_sensor_name)

    # センサ情報取得
    try:
        sensor_item = t_sensor_info.query(
            # GSIの名前を指定
            IndexName='serviceLocationID-updateTimeInfo-index',
            # 固定のパーティションキーを指定
            KeyConditionExpression=Key('serviceLocationID').eq(int(service_location_id)),
            # 降順で最新のデータが先頭に
            ScanIndexForward=False,
            # 最新の1件のみ取得
            Limit=1
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            response_status = 204
            return result, response_status

    # センサ情報取得できた場合
    if sensor_item['Items']:
        # 結果を代入
        sensor_item = sensor_item['Items'][0]

        if 'dataModelType' in sensor_item:
            result['dataModelType'] = str(sensor_item.get('dataModelType'))
        result['attribute'] = {}
        result['attribute']['serviceLocationID'] = int(sensor_item.get('serviceLocationID'))
        result['attribute']['roadsideUnitID'] = int(sensor_item.get('roadsideUnitID'))
        result['attribute']['updateTimeInfo'] = str(sensor_item.get('updateTimeInfo'))
        result['attribute']['formatVersion'] = int(sensor_item.get('formatVersion'))
        result['attribute']['sensorNum'] = int(sensor_item.get('sensorNum'))
        result['attribute']['sensorAttributeInfo'] = ast.literal_eval(sensor_item.get('sensorAttributeInfo'))

    else:
        response_status = 204

    return result, response_status
