# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import logging
import os

import boto3
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
USE_CASE_INFO_TABLE_NAME = os.environ['USE_CASE_INFO_TABLE_NAME']

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key

# DynamoDBテーブルオブジェクト
t_use_case_info = dynamoDB.Table(USE_CASE_INFO_TABLE_NAME)


def get_data(service_location_id, roadside_unit_id):
    """
    ユースケース情報取得
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
        # ユースケース情報取得
        data_list, response_status = get_data_execute(service_location_id, roadside_unit_id, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(service_location_id, roadside_unit_id, response_status):
    """
    ユースケース情報取得
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

    # ユースケース情報取得
    use_case_item = t_use_case_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(int(roadside_unit_id)) & Key('serviceLocationID').eq(int(service_location_id))
    )

    # ユースケース情報取得できた場合
    if use_case_item['Items']:
        # 結果を代入
        use_case_item = use_case_item['Items'][0]

        if 'dataModelType' in use_case_item:
            result['dataModelType'] = str(use_case_item.get('dataModelType'))
        result['attribute'] = {}
        result['attribute']['serviceLocationID'] = int(use_case_item.get('serviceLocationID'))
        result['attribute']['roadsideUnitID'] = int(use_case_item.get('roadsideUnitID'))
        result['attribute']['updateTimeInfo'] = str(use_case_item.get('updateTimeInfo'))
        result['attribute']['formatVersion'] = int(use_case_item.get('formatVersion'))
        result['attribute']['useCaseInfo'] = ast.literal_eval(use_case_item.get('useCaseInfo'))

    else:
        response_status = 204

    return result, response_status
