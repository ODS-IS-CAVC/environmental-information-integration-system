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


def get_data(service_location_id, roadside_unit_id):
    """
    路側機属性情報取得
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
        # 路側機属性情報取得
        data_list, response_status = get_data_execute(service_location_id, roadside_unit_id, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(service_location_id, roadside_unit_id, response_status):
    """
    路側機属性情報取得
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
    result : array
        取得されたデータ
    response_status : int
        処理完了ステータス
    """

    result = {}

    # 路側機属性情報取得
    roadside_unit_item = t_roadside_unit_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(int(roadside_unit_id)) & Key('serviceLocationID').eq(int(service_location_id))
    )

    # 路側機属性情報取得できた場合
    if roadside_unit_item['Items']:
        # 結果を代入
        roadside_unit_item = roadside_unit_item['Items'][0]

        if 'dataModelType' in roadside_unit_item:
            result['dataModelType'] = str(roadside_unit_item.get('dataModelType'))
        result['attribute'] = {}
        result['attribute']['serviceLocationID'] = int(roadside_unit_item.get('serviceLocationID'))
        result['attribute']['roadsideUnitID'] = int(roadside_unit_item.get('roadsideUnitID'))
        result['attribute']['updateTimeInfo'] = str(roadside_unit_item.get('updateTimeInfo'))
        result['attribute']['formatVersion'] = int(roadside_unit_item.get('formatVersion'))
        result['attribute']['roadsideUnitName'] = str(roadside_unit_item.get('roadsideUnitName'))
        result['attribute']['productNumber'] = str(roadside_unit_item.get('productNumber'))
        if 'manufacturer' in roadside_unit_item:
            result['attribute']['manufacturer'] = str(roadside_unit_item.get('manufacturer'))
        if 'customer' in roadside_unit_item:
            result['attribute']['customer'] = str(roadside_unit_item.get('customer'))
        result['attribute']['licensingInfo'] = str(roadside_unit_item.get('licensingInfo'))
        result['attribute']['initialRegistrationDate'] = str(roadside_unit_item.get('initialRegistrationDate'))
        result['attribute']['powerConsumption'] = int(roadside_unit_item.get('powerConsumption'))
        result['attribute']['grossWeight'] = int(roadside_unit_item.get('grossWeight'))
        result['attribute']['materialType'] = int(roadside_unit_item.get('materialType'))
        result['attribute']['dateOfInstallation'] = str(roadside_unit_item.get('dateOfInstallation'))
        result['attribute']['latitude'] = int(roadside_unit_item.get('latitude'))
        result['attribute']['longitude'] = int(roadside_unit_item.get('longitude'))
        result['attribute']['roadsideUnitManager'] = str(roadside_unit_item.get('roadsideUnitManager'))
        result['attribute']['installationSiteManager'] = str(roadside_unit_item.get('installationSiteManager'))
        result['attribute']['lastInspectionDate'] = str(roadside_unit_item.get('lastInspectionDate'))
        result['attribute']['nextInspectionDate'] = str(roadside_unit_item.get('nextInspectionDate'))

    else:
        response_status = 204

    return result, response_status
