# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os

import boto3
from botocore.exceptions import ClientError
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
SENSOR_INFO_TABLE_NAME = os.environ['SENSOR_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')


def put_data(parameters):
    """
    センサ情報登録
    parameters
    ----------
    parameters : array
        センサ情報パラメータ

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    try:
        base_table_name = SENSOR_INFO_TABLE_NAME
        table_name = f"{base_table_name}_{parameters['attribute']['roadsideUnitID']}"
        t_sensor_info = dynamoDB.Table(table_name)

        # プライマリキー(time_minutes, updateTimeInfo)の重複を防ぐためserviceLocationIDを末尾に結合
        unique_update_time_info = f"{parameters['attribute']['updateTimeInfo']}_{parameters['attribute']['serviceLocationID']}"

        # センサ情報登録
        item = {
            'time_minutes': parameters['attribute']['time_minutes'],
            'unique_updateTimeInfo': unique_update_time_info,
            'serviceLocationID': parameters['attribute']['serviceLocationID'],
            'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
            'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
            'formatVersion': parameters['attribute']['formatVersion'],
            'sensorNum': parameters['attribute']['sensorNum'],
            'sensorAttributeInfo': str(parameters['attribute']['sensorAttributeInfo'])
        }
        if 'dataModelType' in parameters:
            item['dataModelType'] = parameters['dataModelType']

        try:
            t_sensor_info.put_item(
                Item=item
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('Not Found ' + table_name)

    except Exception:
        logger.error('other error')
        raise

    return response_status
