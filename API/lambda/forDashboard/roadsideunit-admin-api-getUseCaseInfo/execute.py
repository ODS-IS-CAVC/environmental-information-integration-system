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


def get_data():
    """
    ユースケース情報全件取得
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
        # ユースケース情報全件取得
        data_list, response_status = get_data_execute(response_status)
    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(response_status):
    """
    ユースケース情報全件取得
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

    # ユースケース情報全件取得
    response = t_use_case_info.scan()

    use_case_items = response['Items']

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループする
    while 'LastEvaluatedKey' in response:
        response = t_use_case_info.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        use_case_items.extend(response['Items'])

    # ユースケース情報取得できた場合
    if len(use_case_items) != 0:
        # 結果を代入
        for use_case_item in use_case_items:
            temporary_result = {}
            if 'dataModelType' in use_case_item:
                temporary_result['dataModelType'] = str(use_case_item.get('dataModelType'))

            temporary_result['attribute'] = {}
            temporary_result['attribute']['serviceLocationID'] = int(use_case_item.get('serviceLocationID'))
            temporary_result['attribute']['roadsideUnitID'] = int(use_case_item.get('roadsideUnitID'))
            temporary_result['attribute']['updateTimeInfo'] = str(use_case_item.get('updateTimeInfo'))
            temporary_result['attribute']['formatVersion'] = int(use_case_item.get('formatVersion'))
            temporary_result['attribute']['useCaseInfo'] = ast.literal_eval(use_case_item.get('useCaseInfo'))
            result.append(temporary_result)
    else:
        response_status = 204
    return result, response_status
