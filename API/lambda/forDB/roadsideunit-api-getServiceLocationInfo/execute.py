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

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_service_location_info = dynamoDB.Table(SERVICE_LOCATION_INFO_TABLE_NAME)


def get_data(service_location_id):
    """
    サービス地点情報取得
    Parameters
    ----------
    service_location_id : int
        サービス地点情報

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
        # サービス地点情報取得
        data_list, response_status = get_data_execute(service_location_id, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(service_location_id, response_status):
    """
    サービス地点情報取得
    Parameters
    ----------
    service_location_id : int
        サービス地点情報ID
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

    # サービス地点情報取得
    service_location_items = t_service_location_info.query(
        # GSIの名前を指定
        IndexName='serviceLocationID-updateTimeInfo-index',
        # 固定のパーティションキーを指定
        KeyConditionExpression=Key('serviceLocationID').eq(int(service_location_id)),
        # 降順で最新のデータを先頭にする
        ScanIndexForward=False
    )

    # サービス地点情報取得できた場合
    if service_location_items['Items']:

        is_first = True
        roadside_unit_list = []
        for service_location_item in service_location_items['Items']:
            # 最初のループのみroadsideUnitList以外の項目を代入
            if is_first is True:
                if 'dataModelType' in service_location_item:
                    result['dataModelType'] = service_location_item['dataModelType']
                result['attribute'] = {}
                result['attribute']['updateTimeInfo'] = service_location_item['updateTimeInfo']
                result['attribute']['formatVersion'] = service_location_item['formatVersion']
                result['attribute']['serviceLocationID'] = service_location_item['serviceLocationID']
                result['attribute']['latitude'] = service_location_item['latitude']
                result['attribute']['longitude'] = service_location_item['longitude']
                result['attribute']['elevation'] = service_location_item['elevation']
                result['attribute']['approachAttributeSize'] = service_location_item['approachAttributeSize']
                result['attribute']['approachAttributeInfo'] = ast.literal_eval(service_location_item['approachAttributeInfo'])
                result['attribute']['roadsideUnitList'] = []
                is_first = False

            # 全てのループでroadsideUnitListに項目を代入
            result_roadside_unit_list = {
                'roadsideUnitID': service_location_item['roadsideUnitID'],
                'roadsideUnitClassification': service_location_item['roadsideUnitClassification']
            }

            roadside_unit_list.append(result_roadside_unit_list)

        roadside_unit_list = sorted(roadside_unit_list, key=lambda x: x['roadsideUnitID'])
        result['attribute']['roadsideUnitList'] = roadside_unit_list

    else:
        response_status = 204

    return result, response_status
