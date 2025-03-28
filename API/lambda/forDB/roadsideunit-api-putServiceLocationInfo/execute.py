# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os

import boto3
import create_table
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
SERVICE_LOCATION_INFO_TABLE_NAME = os.environ['SERVICE_LOCATION_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_service_location_info = dynamoDB.Table(SERVICE_LOCATION_INFO_TABLE_NAME)


def put_data(parameters):
    """
    サービス地点情報作成
    parameters
    ----------
    parameters : Array
        サービス地点情報パラメータ

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    try:
        # roadsideUnitListの数だけ登録更新処理
        for roadside_unit_value in parameters['attribute']['roadsideUnitList']:
            # サービス地点情報の判別フラグ取得
            data_exists_flag = get_data(roadside_unit_value['roadsideUnitID'], parameters['attribute']['serviceLocationID'])

            # 既存のサービス地点情報が一件でも存在していればステータス更新
            if data_exists_flag is True:
                response_status = 200

            # 既存のサービス地点情報が存在していなければテーブル新規作成
            else:
                # 各テーブル作成
                create_table.create_dynamodb_table(roadside_unit_value['roadsideUnitID'], parameters['attribute']['serviceLocationID'])

            # サービス地点情報登録
            item = {
                'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
                'formatVersion': parameters['attribute']['formatVersion'],
                'serviceLocationID': parameters['attribute']['serviceLocationID'],
                'latitude': parameters['attribute']['latitude'],
                'longitude': parameters['attribute']['longitude'],
                'elevation': parameters['attribute']['elevation'],
                'approachAttributeSize': parameters['attribute']['approachAttributeSize'],
                'approachAttributeInfo': str(parameters['attribute']['approachAttributeInfo']),
                'roadsideUnitID': roadside_unit_value['roadsideUnitID'],
                'roadsideUnitClassification': roadside_unit_value['roadsideUnitClassification'],
            }
            if 'dataModelType' in parameters:
                item['dataModelType'] = parameters['dataModelType']

            t_service_location_info.put_item(
                Item=item
            )

    except Exception:
        logger.error('other error')
        raise

    return response_status


def get_data(roadside_unit_id, service_location_id):
    """
    指定されたIDのサービス地点情報が存在するか判別する
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID

    Returns
    -------
    data_exists_flag : bool
        サービス地点情報判別フラグ
    """

    data_exists_flag = False

    # サービス地点情報取得
    service_location_items = t_service_location_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(roadside_unit_id) & Key('serviceLocationID').eq(service_location_id)
    )
    service_location_items = service_location_items.get('Items', [])

    # サービス地点情報が存在していればTrueを返す
    if len(service_location_items) != 0:
        data_exists_flag = True

    return data_exists_flag
