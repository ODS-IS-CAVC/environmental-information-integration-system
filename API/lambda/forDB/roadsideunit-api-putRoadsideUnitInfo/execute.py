# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
ROADSIDE_UNIT_INFO_TABLE_NAME = os.environ['ROADSIDE_UNIT_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_roadside_unit_info = dynamoDB.Table(ROADSIDE_UNIT_INFO_TABLE_NAME)


def put_data(parameters, data_exists_flag):
    """
    路側機属性情報登録
    parameters
    ----------
    parameters : Array
        路側機属性情報パラメータ
    data_exists_flag : bool
        路側機属性情報判別フラグ

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    # 更新処理の場合はステータス200を返す
    if data_exists_flag is True:
        response_status = 200

    try:
        # 路側機属性情報登録
        item = {
            'serviceLocationID': parameters['attribute']['serviceLocationID'],
            'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
            'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
            'formatVersion': parameters['attribute']['formatVersion'],
            'roadsideUnitName': parameters['attribute']['roadsideUnitName'],
            'productNumber': parameters['attribute']['productNumber'],
            'licensingInfo': parameters['attribute']['licensingInfo'],
            'initialRegistrationDate': parameters['attribute']['initialRegistrationDate'],
            'powerConsumption': parameters['attribute']['powerConsumption'],
            'grossWeight': parameters['attribute']['grossWeight'],
            'materialType': parameters['attribute']['materialType'],
            'dateOfInstallation': parameters['attribute']['dateOfInstallation'],
            'latitude': parameters['attribute']['latitude'],
            'longitude': parameters['attribute']['longitude'],
            'roadsideUnitManager': parameters['attribute']['roadsideUnitManager'],
            'installationSiteManager': parameters['attribute']['installationSiteManager'],
            'lastInspectionDate': parameters['attribute']['lastInspectionDate'],
            'nextInspectionDate': parameters['attribute']['nextInspectionDate'],
        }
        if 'dataModelType' in parameters:
            item['dataModelType'] = parameters['dataModelType']
        if 'manufacturer' in parameters['attribute']:
            item['manufacturer'] = parameters['attribute']['manufacturer']
        if 'customer' in parameters['attribute']:
            item['customer'] = parameters['attribute']['customer']

        t_roadside_unit_info.put_item(
            Item=item
        )

    except Exception:
        logger.error('other error')
        raise

    return response_status


def get_data(roadside_unit_id, service_location_id):
    """
    指定されたIDの路側機属性情報が存在するか判別する
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID

    Returns
    -------
    data_exists_flag : bool
        路側機属性情報判別フラグ
    """

    data_exists_flag = False

    # 路側機属性情報取得
    roadside_unit_items = t_roadside_unit_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(roadside_unit_id) & Key('serviceLocationID').eq(service_location_id)
    )
    roadside_unit_items = roadside_unit_items.get('Items', [])

    # 路側機属性情報が存在していればTrueを返す
    if len(roadside_unit_items) != 0:
        data_exists_flag = True

    return data_exists_flag
