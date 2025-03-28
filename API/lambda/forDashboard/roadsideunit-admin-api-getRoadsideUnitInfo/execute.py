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


def get_data():
    """
    路側機属性情報全件取得
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
        # 路側機属性情報全件取得
        data_list, response_status = get_data_execute(response_status)
    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(response_status):
    """
    路側機属性情報全件取得
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

    # 路側機属性情報全件取得
    response = t_roadside_unit_info.scan()

    roadside_unit_items = response['Items']

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループする
    while 'LastEvaluatedKey' in response:
        response = t_roadside_unit_info.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        roadside_unit_items.extend(response['Items'])

    # 路側機属性情報取得できた場合
    if len(roadside_unit_items) != 0:
        # 結果を代入
        for roadside_unit_item in roadside_unit_items:
            temporary_result = {}
            if 'dataModelType' in roadside_unit_item:
                temporary_result['dataModelType'] = str(roadside_unit_item.get('dataModelType'))
            temporary_result['attribute'] = {}
            temporary_result['attribute']['serviceLocationID'] = int(roadside_unit_item.get('serviceLocationID'))
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
    else:
        response_status = 204
    return result, response_status
