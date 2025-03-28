# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
SERVICE_LOCATION_INFO_TABLE_NAME = os.environ['SERVICE_LOCATION_INFO_TABLE_NAME']
ROADSIDE_UNIT_INFO_TABLE_NAME = os.environ['ROADSIDE_UNIT_INFO_TABLE_NAME']


# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_service_location_info = dynamoDB.Table(SERVICE_LOCATION_INFO_TABLE_NAME)
t_roadside_unit_info = dynamoDB.Table(ROADSIDE_UNIT_INFO_TABLE_NAME)


def get_data():
    """
    サービス地点情報全件取得
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
        # サービス地点情報全件取得
        data_list, response_status = get_data_execute(response_status)
    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(response_status):
    """
    サービス地点情報全件取得
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

    # サービス地点情報全件取得
    response = t_service_location_info.scan()

    service_location_items = response['Items']

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループする
    while 'LastEvaluatedKey' in response:
        response = t_service_location_info.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        service_location_items.extend(response['Items'])

    # サービス地点情報取得できた場合
    if len(service_location_items) != 0:
        service_location_items = sorted(service_location_items, key=lambda x: x['serviceLocationID'])

        temporary_service_location_id = 0
        # 結果を代入
        for service_location_item in service_location_items:
            temporary_result = {}
            # 前回ループで保持したサービス地点IDと別のサービス地点IDの場合
            if temporary_service_location_id != service_location_item['serviceLocationID']:

                temporary_service_location_id = service_location_item['serviceLocationID']

                if 'dataModelType' in service_location_item:
                    temporary_result['dataModelType'] = service_location_item['dataModelType']
                temporary_result['attribute'] = {}
                temporary_result['attribute']['updateTimeInfo'] = service_location_item['updateTimeInfo']
                temporary_result['attribute']['formatVersion'] = service_location_item['formatVersion']
                temporary_result['attribute']['serviceLocationID'] = service_location_item['serviceLocationID']
                temporary_result['attribute']['latitude'] = service_location_item['latitude']
                temporary_result['attribute']['longitude'] = service_location_item['longitude']
                temporary_result['attribute']['elevation'] = service_location_item['elevation']
                temporary_result['attribute']['approachAttributeSize'] = service_location_item['approachAttributeSize']
                temporary_result['attribute']['approachAttributeInfo'] = ast.literal_eval(service_location_item['approachAttributeInfo'])

                # サービス地点IDに紐づく路側機属性情報を取得
                roadside_unit_list = get_roadside_unit_execute(service_location_item['serviceLocationID'])
                temporary_result['attribute']['roadsideUnitList'] = roadside_unit_list
                result.append(temporary_result)
    else:
        response_status = 204
    return result, response_status


def get_roadside_unit_execute(service_location_id):
    """
    路側機属性情報取得
    Parameters
    ----------
    service_location_id : int
        サービス地点ID

    Returns
    -------
    result : array
        取得されたデータ
    """
    result = []

    response = t_roadside_unit_info.query(
        # GSIの名前を指定
        IndexName='serviceLocationID-roadsideUnitID-index',
        # 固定のパーティションキーを指定
        KeyConditionExpression=Key('serviceLocationID').eq(int(service_location_id)),
    )
    roadside_unit_items = response['Items']

    # 結果を代入
    for roadside_unit_item in roadside_unit_items:
        temporary_result = {}
        if 'dataModelType' in roadside_unit_item:
            temporary_result['dataModelType'] = str(roadside_unit_item.get('dataModelType'))
        temporary_result['attribute'] = {}
        temporary_result['attribute']['roadsideUnitID'] = int(roadside_unit_item.get('roadsideUnitID'))
        temporary_result['attribute']['updateTimeInfo'] = str(roadside_unit_item.get('updateTimeInfo'))
        temporary_result['attribute']['formatVersion'] = int(roadside_unit_item.get('formatVersion'))
        temporary_result['attribute']['roadsideUnitName'] = str(roadside_unit_item.get('roadsideUnitName'))
        temporary_result['attribute']['productNumber'] = str(roadside_unit_item.get('productNumber'))
        if 'manufacturer' in roadside_unit_item:
            temporary_result['attribute']['manufacturer'] = str(roadside_unit_item.get('manufacturer'))
        if 'customer' in roadside_unit_item:
            temporary_result['attribute']['customer'] = str(roadside_unit_item.get('customer'))
        temporary_result['attribute']['licensingInfo'] = str(roadside_unit_item.get('licensingInfo'))
        temporary_result['attribute']['initialRegistrationDate'] = str(roadside_unit_item.get('initialRegistrationDate'))
        temporary_result['attribute']['powerConsumption'] = int(roadside_unit_item.get('powerConsumption'))
        temporary_result['attribute']['grossWeight'] = int(roadside_unit_item.get('grossWeight'))
        temporary_result['attribute']['materialType'] = int(roadside_unit_item.get('materialType'))
        temporary_result['attribute']['dateOfInstallation'] = str(roadside_unit_item.get('dateOfInstallation'))
        temporary_result['attribute']['latitude'] = int(roadside_unit_item.get('latitude'))
        temporary_result['attribute']['longitude'] = int(roadside_unit_item.get('longitude'))
        temporary_result['attribute']['roadsideUnitManager'] = str(roadside_unit_item.get('roadsideUnitManager'))
        temporary_result['attribute']['installationSiteManager'] = str(roadside_unit_item.get('installationSiteManager'))
        temporary_result['attribute']['lastInspectionDate'] = str(roadside_unit_item.get('lastInspectionDate'))
        temporary_result['attribute']['nextInspectionDate'] = str(roadside_unit_item.get('nextInspectionDate'))
        result.append(temporary_result)

    return result
