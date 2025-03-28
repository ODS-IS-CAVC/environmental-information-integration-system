import logging
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
TARGET_INFO_TABLE_NAME = os.environ['TARGET_INFO_TABLE_NAME']
RECORD_MAX_TARGET = int(os.environ['RECORD_MAX_TARGET'])

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')


def put_data(parameters):
    """
    物標情報登録
    parameters
    ----------
    parameters : Array
        物標情報パラメータ

    Returns
    -------
    response_status : int
        処理完了ステータス
    """

    response_status = 201

    try:
        # 登録する物標情報テーブル名を作成
        base_table_name = TARGET_INFO_TABLE_NAME
        t_target_name = f"{base_table_name}_{parameters['attribute']['roadsideUnitID']}_{parameters['attribute']['serviceLocationID']}"
        t_target_info = dynamoDB.Table(t_target_name)

        # 物標情報登録
        for device_individual_value in parameters['attribute']['deviceIndividualInfo']:
            if 'targetIndividualInfo' in device_individual_value:
                # timeで昇順にソート
                device_individual_value['targetIndividualInfo'] = sorted(device_individual_value['targetIndividualInfo'], key=lambda x: getTimeUtc(x["time"]))

                # 100物標ずつの配列を生成
                split_array = [device_individual_value['targetIndividualInfo'][i:i + RECORD_MAX_TARGET] for i in range(0, len(device_individual_value['targetIndividualInfo']), RECORD_MAX_TARGET)]

                for split_target_individual_value in split_array:
                    # プライマリーキー(time_minutes,time)の重複を防ぐためtargetIDを末尾に結合
                    unique_time = f"{split_target_individual_value[0]['time']}_{split_target_individual_value[0]['targetID']}"

                    # 物標情報登録
                    item = {
                        'time_minutes': getTimeMinutes(split_target_individual_value[0]['time']),
                        'unique_time': unique_time,
                        'roadsideUnitID': parameters['attribute']['roadsideUnitID'],
                        'serviceLocationID': parameters['attribute']['serviceLocationID'],
                        'updateTimeInfo': parameters['attribute']['updateTimeInfo'],
                        'formatVersion': parameters['attribute']['formatVersion'],
                        'deviceID': device_individual_value['deviceID'],
                        'time_utc': getTimeUtc(split_target_individual_value[0]['time']),
                        'targetIndividualInfo': str(split_target_individual_value),
                    }
                    if 'dataModelType' in parameters:
                        item['dataModelType'] = parameters['dataModelType']

                    try:
                        t_target_info.put_item(
                            Item=item
                        )
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'ResourceNotFoundException':
                            logger.error('Not Found ' + t_target_name)
    except Exception:
        logger.error('other error')
        raise

    return response_status


def getTimeMinutes(time):
    """
    時刻「分」までをフォーマットで取得
    Parameters
    ----------
    time : string
        時刻情報

    Returns
    -------
    format_time  : String
        時刻「分」まで時刻情報
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')
    # 時刻「分」までをフォーマットで取得
    format_time = time.strftime('%Y-%m-%d %H:%M')

    return format_time


def getTimeUtc(time):
    """
    タイムゾーンをutcに変換
    Parameters
    ----------
    time : string
        時刻情報

    Returns
    -------
    utc_time  : String
        時刻をUTCに変換
    """
    # iso形式の文字列をdatetimeオブジェクトに変換
    iso_time = datetime.fromisoformat(time)

    # タイムゾーンをutcに変換
    utc_time = iso_time.astimezone(timezone.utc)

    # フォーマットを整える
    utc_time = utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return utc_time
