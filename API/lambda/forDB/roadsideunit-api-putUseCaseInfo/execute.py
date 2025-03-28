# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

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


def put_data(parameters, data_exists_flag):
    """
    ユースケース情報登録
    parameters
    ----------
    parameters : Array
        ユースケース情報パラメータ
    data_exists_flag : bool
        ユースケース情報判別フラグ

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
        # ユースケース情報登録
        item = {
            'serviceLocationID': parameters['attribute']['serviceLocationID'],
            'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
            'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
            'formatVersion': parameters['attribute']['formatVersion'],
            'useCaseInfo': str(parameters['attribute']['useCaseInfo'])
        }
        if 'dataModelType' in parameters:
            item['dataModelType'] = parameters['dataModelType']

        t_use_case_info.put_item(
            Item=item
        )

    except Exception:
        logger.error('other error')
        raise

    return response_status


def get_data(roadside_unit_id, service_location_id):
    """
    指定されたIDのユースケース情報が存在するか判別する
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID

    Returns
    -------
    data_exists_flag : bool
        ユースケース情報判別フラグ
    """

    data_exists_flag = False

    # ユースケース情報取得
    use_case_items = t_use_case_info.query(
        KeyConditionExpression=Key('roadsideUnitID').eq(roadside_unit_id) & Key('serviceLocationID').eq(service_location_id)
    )
    use_case_items = use_case_items.get('Items', [])

    # ユースケース情報が存在していればTrueを返す
    if len(use_case_items) != 0:
        data_exists_flag = True

    return data_exists_flag
