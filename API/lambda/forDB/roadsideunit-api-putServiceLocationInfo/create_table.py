# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')

# 環境変数取得
SENSOR_INFO_TABLE_NAME = os.environ['SENSOR_INFO_TABLE_NAME']
ALIVE_MONITORING_INFO_TABLE_NAME = os.environ['ALIVE_MONITORING_INFO_TABLE_NAME']
TARGET_INFO_TABLE_NAME = os.environ['TARGET_INFO_TABLE_NAME']


def create_dynamodb_table(roadside_unit_id, service_location_id):
    """
    各テーブルを作成
    parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    """
    try:
        # DynamoDBのすべてのテーブル名を取得
        existing_tables = [table.name for table in dynamoDB.tables.all()]

        # 作成するテーブルのテーブル名を定義
        sensor_table_name = f"{SENSOR_INFO_TABLE_NAME}_{roadside_unit_id}"
        alive_monitoring_table_name = f"{ALIVE_MONITORING_INFO_TABLE_NAME}_{roadside_unit_id}"
        target_table_name = f"{TARGET_INFO_TABLE_NAME}_{roadside_unit_id}_{service_location_id}"

        # 定義したテーブル名のテーブルが存在しない場合作成
        if sensor_table_name not in existing_tables:
            # センサ情報テーブル作成
            create_sensor_table(sensor_table_name)

        if alive_monitoring_table_name not in existing_tables:
            # 死活監視情報テーブル作成
            create_alive_monitoring_table(alive_monitoring_table_name)

        if target_table_name not in existing_tables:
            # 物標情報テーブル作成
            create_target_table(target_table_name)

    except Exception:
        logger.error('other error')
        raise


def create_sensor_table(sensor_table_name):
    """
    センサ情報テーブル作成
    parameters
    ----------
    sensor_table_name : str
        センサ情報テーブル名
    """

    dynamoDB.create_table(
        TableName=sensor_table_name,
        KeySchema=[
            {'AttributeName': 'time_minutes', 'KeyType': 'HASH'},
            {'AttributeName': 'unique_updateTimeInfo', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'time_minutes', 'AttributeType': 'S'},
            {'AttributeName': 'unique_updateTimeInfo', 'AttributeType': 'S'},
            {'AttributeName': 'serviceLocationID', 'AttributeType': 'N'},
            {'AttributeName': 'updateTimeInfo', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST',
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'serviceLocationID-updateTimeInfo-index',
                'KeySchema': [
                    {'AttributeName': 'serviceLocationID', 'KeyType': 'HASH'},
                    {'AttributeName': 'updateTimeInfo', 'KeyType': 'RANGE'},
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
            }
        ]
    )


def create_alive_monitoring_table(alive_monitoring_table_name):
    """
    死活監視情報テーブル作成
    parameters
    ----------
    alive_monitoring_table_name : str
        死活監視情報テーブル名
    """

    dynamoDB.create_table(
        TableName=alive_monitoring_table_name,
        KeySchema=[
            {'AttributeName': 'time_minutes', 'KeyType': 'HASH'},
            {'AttributeName': 'unique_updateTimeInfo', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'time_minutes', 'AttributeType': 'S'},
            {'AttributeName': 'unique_updateTimeInfo', 'AttributeType': 'S'},
        ],
        BillingMode='PAY_PER_REQUEST',
    )


def create_target_table(target_table_name):
    """
    物標情報テーブル作成
    parameters
    ----------
    target_table_name : str
        物標情報テーブル名
    """

    dynamoDB.create_table(
        TableName=target_table_name,
        KeySchema=[
            {'AttributeName': 'time_minutes', 'KeyType': 'HASH'},
            {'AttributeName': 'unique_time', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'time_minutes', 'AttributeType': 'S'},
            {'AttributeName': 'unique_time', 'AttributeType': 'S'},
            {'AttributeName': 'deviceID', 'AttributeType': 'N'},
            {'AttributeName': 'time_utc', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST',
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'deviceID-time_utc-index',
                'KeySchema': [
                    {'AttributeName': 'deviceID', 'KeyType': 'HASH'},
                    {'AttributeName': 'time_utc', 'KeyType': 'RANGE'},
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
            }
        ]
    )
