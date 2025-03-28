# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import logging
import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone

import boto3
import pandas as pd
from botocore.exceptions import ClientError
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# 環境変数取得
TARGET_INFO_TABLE_NAME = os.environ['TARGET_INFO_TABLE_NAME']
SENSOR_INFO_TABLE_NAME = os.environ['SENSOR_INFO_TABLE_NAME']
MAX_DEVICE_NUM = int(os.environ['MAX_DEVICE_NUM'])
MAX_TARGET_NUM = int(os.environ['MAX_TARGET_NUM'])
RANGE_SECONDS = int(os.environ['RANGE_SECONDS'])

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key


def get_data(roadside_unit_id, service_location_id, query_params):
    """
    物標情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    query_params : list
        クエリパラメータ

    Returns
    -------
    data_list : Array
        データ返却用配列
    response_status : int
        処理完了ステータス
    """

    data_list = []
    response_status = 200

    try:
        # 物標情報取得
        data_list, response_status = get_data_execute(roadside_unit_id, service_location_id, query_params, response_status)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(roadside_unit_id, service_location_id, query_params, response_status):
    """
    物標情報取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    query_params : list
        クエリパラメータ
    response_status : int
        処理完了ステータス

    Returns
    -------
    result : Array
        取得されたデータ
    response_status : 200:正常終了 204:データ未取得
    """

    # 取得する物標情報テーブル名を作成
    base_table_name = TARGET_INFO_TABLE_NAME
    t_target_name = f"{base_table_name}_{roadside_unit_id}_{service_location_id}"

    t_target_info = dynamoDB.Table(t_target_name)

    # 物標情報を整形し、取得
    result, response_status = get_target_value(roadside_unit_id, service_location_id, t_target_info, response_status, query_params)

    return result, response_status


def get_target_value(roadside_unit_id, service_location_id, t_target_info, response_status, query_params):
    """
    物標情報を整形し、取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    t_target_info
        物標情報テーブル
    response_status : int
        路側機ID
    query_params : list
        クエリパラメータ

    Returns
    -------
    result : Array
        取得されたデータ
    response_status : int
    """

    result = {}

    deviceIndividualInfo_template = {
        'deviceID': 0,
        'targetNum': 0,
        'targetIndividualInfo': []
    }
    is_first = True
    device_ids = []

    # 最新の機器種別IDを取得
    device_ids = get_device_ids(roadside_unit_id, service_location_id, device_ids, query_params)

    if len(device_ids) != 0:
        for device_id in device_ids:
            # クエリの取得
            target_query = get_query_items(query_params, device_id)
            # クエリの実行
            try:
                response = t_target_info.query(**target_query)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    response_status = 204
                    return result, response_status

            target_items = response['Items']

            if len(target_items) != 0:
                filter_target_items = get_filter_target_items(target_items, query_params)
                if len(filter_target_items) != 0:
                    # 最初のループのみdeviceIndividualInfo以外の項目を代入
                    if is_first is True:
                        if 'startAt' in query_params:
                            array_number = -1
                        else:
                            array_number = 0
                        if 'dataModelType' in target_items[array_number]:
                            result['dataModelType'] = str(target_items[array_number]['dataModelType'])
                        result['attribute'] = {}
                        result['attribute']['serviceLocationID'] = int(target_items[array_number]['serviceLocationID'])
                        result['attribute']['roadsideUnitID'] = int(target_items[array_number]['roadsideUnitID'])
                        result['attribute']['updateTimeInfo'] = str(target_items[array_number]['updateTimeInfo'])
                        result['attribute']['formatVersion'] = int(target_items[array_number]['formatVersion'])
                        result['attribute']['deviceNum'] = 0
                        result['attribute']['deviceIndividualInfo'] = []
                        is_first = False
                    # 機器情報を初期化
                    deviceIndividualInfo = deepcopy(deviceIndividualInfo_template)

                    for filter_target_item in filter_target_items:
                        deviceIndividualInfo['deviceID'] = filter_target_item['deviceID']

                        deviceIndividualInfo['targetIndividualInfo'].append(filter_target_item['targetIndividualInfo'])

                    # ループの結果を代入
                    deviceIndividualInfo['targetNum'] = len(deviceIndividualInfo['targetIndividualInfo'])
                    result['attribute']['deviceIndividualInfo'].append(deviceIndividualInfo)
        if is_first is False:
            result['attribute']['deviceNum'] = len(result['attribute']['deviceIndividualInfo'])

    if is_first is True:
        response_status = 204

    return result, response_status


def get_query_items(query_params, device_id):
    """
    物標情報のクエリを取得
    Parameters
    ----------
    query_params : list
        クエリパラメータ
    device_id : int
        機器種別ID

    Returns
    -------
    query : dict
        取得されたデータ
    """
    index_name = 'deviceID-time_utc-index'
    key_name = 'deviceID'
    equal_key = int(device_id)

    query = {
        'IndexName': index_name,
        'KeyConditionExpression': Key(key_name).eq(equal_key),
        'Limit': MAX_TARGET_NUM
    }

    # 両方指定された場合、古い順から取得
    if 'startAt' in query_params and 'endAt' in query_params:
        query['KeyConditionExpression'] &= Key('time_utc').between(getTimeUtc(query_params['startAt'], 'start_at'), getTimeUtc(query_params['endAt'], 'end_at'))
        query['ScanIndexForward'] = True

    # start_atのみ指定された場合、古い順から取得
    elif 'startAt' in query_params:
        query['KeyConditionExpression'] &= Key('time_utc').gte(getTimeUtc(query_params['startAt'], 'start_at'))
        query['ScanIndexForward'] = True

    # end_atのみ指定された場合、新しい順から取得
    elif 'endAt' in query_params:
        query['KeyConditionExpression'] &= Key('time_utc').lte(getTimeUtc(query_params['endAt'], 'end_at'))
        query['ScanIndexForward'] = False

    return query


def get_filter_target_items(target_items, query_params):
    """
    配列からデータを取り出して正確な時刻にて再検索
    Parameters
    ----------
    target_items
        物標情報データ
    query_params: list
        クエリパラメータ

    Returns
    -------
    result : dict
        再検索されたデータ
    """

    dfs = []
    for target_item in target_items:
        target_info_list = ast.literal_eval(target_item["targetIndividualInfo"])
        # 物標情報をDataFrameに変換
        if target_info_list:
            target_info_df = pd.DataFrame(target_info_list)

            device_id_data = {
                'deviceID': target_item['deviceID'] for key in target_item
            }
            # 機器種別IDのみdictをDataFrameに変換
            device_id_data_df = pd.DataFrame([device_id_data] * len(target_info_df))

            # 物標情報と機器種別IDのDataFrameを結合
            combined_df = pd.concat([device_id_data_df, target_info_df], axis=1)
            # 結果をリストに追加
            dfs.append(combined_df)

    # 全レコードを統合
    df = pd.concat(dfs, ignore_index=True)

    df["time"] = pd.to_datetime(df["time"], format='%Y-%m-%dT%H:%M:%S.%f%z')

    if 'startAt' in query_params:
        start_at = query_params['startAt'].replace(" ", "+")
        format_start_at = datetime.fromisoformat(start_at)
    if 'endAt' in query_params:
        end_at = query_params['endAt'].replace(" ", "+")
        format_end_at = datetime.fromisoformat(end_at)

    # 両方指定された場合、古い順から取得
    if 'startAt' in query_params and 'endAt' in query_params:
        filtered_df = df[(df["time"] >= format_start_at) & (df["time"] <= format_end_at)]
        filtered_df = filtered_df.sort_values(by="time")

    # start_atのみ指定された場合、古い順から取得
    elif 'startAt' in query_params:
        filtered_df = df[(df["time"] >= format_start_at)]
        filtered_df = filtered_df.sort_values(by="time")

    # end_atのみ指定された場合、新しい順から取得
    elif 'endAt' in query_params:
        filtered_df = df[(df["time"] <= format_end_at)]
        filtered_df = filtered_df.sort_values(by="time", ascending=False)

    # 機器種別ごとの上限の物標情報のみ抽出
    filtered_df = filtered_df.head(MAX_TARGET_NUM)

    # 各キーを定義
    info_keys = ['commonServiceStandardID', 'targetMessageID', 'targetIndividualVersionInfo', 'targetID', 'targetIndividualIncrementCounter', 'dataLength', 'individualOptionFlag', 'leapSecondCorrectionInfo', 'time', 'latitude', 'longitude', 'elevation', 'positionConf', 'elevationConf', 'speed', 'heading', 'acceleration', 'speedConf', 'headingConf', 'forwardRearAccelerationConf', 'transmissionState', 'steeringWheelAngle', 'sizeClassification', 'roleClassification', 'vehicleWidth', 'vehicleLength', 'positionDelay', 'revisionCounter', 'roadFacilities', 'roadClassification', 'semiMajorAxisOfPositionalErrorEllipse', 'semiMinorAxisOfPositionalErrorEllipse', 'semiMajorAxisOrientationOfPositionalErrorEllipse', 'GPSPositioningMode', 'GPSPDOP', 'numberOfGPSSatellitesInUse', 'GPSMultiPathDetection', 'deadReckoningAvailability', 'mapMatchingAvailability', 'yawRate', 'brakeAppliedStatus', 'auxiliaryBrakeAppliedStatus', 'throttlePosition', 'exteriorLights', 'adaptiveCruiseControlStatus', 'cooperativeAdaptiveCruiseControlStatus', 'preCrashSafetyStatus', 'antilockBrakeStatus', 'tractionControlStatus', 'electronicStabilityControlStatus', 'laneKeepingAssistStatus', 'laneDepartureWarningStatus', 'intersectionDistanceInformationAvailability', 'intersectionDistance', 'intersectionPositionInformationAvailability', 'intersectionLatitude', 'intersectionLongitude', 'extendedInformation', 'targetIndividualExtendedData', 'restingState', 'existingTime']
    # 各レコードを辞書としてリスト化
    result = []
    for _, row in filtered_df.iterrows():
        target_individual_info = {}
        for key in info_keys:
            # キーが存在し、値がある場合のみ処理を実行
            if key in row and not pd.isna(row[key]):
                # "time" の場合は isoformat() を使用、それ以外はそのままの値を取得
                target_individual_info[key] = row[key].isoformat() if key == "time" else row.get(key)

        result.append({
            "deviceID": row["deviceID"],
            "targetIndividualInfo": target_individual_info
        })
    return result


def getTimeUtc(time, search_parameter):
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
    # パラメータの値を変更
    format_time = time.replace(" ", "+")

    # iso形式の文字列をdatetimeオブジェクトに変換
    iso_time = datetime.fromisoformat(format_time)

    # タイムゾーンをutcに変換
    utc_time = iso_time.astimezone(timezone.utc)

    # start_atが指定された場合時刻から1秒引く
    if 'start_at' in search_parameter:
        utc_time = utc_time - timedelta(seconds=RANGE_SECONDS)
    # end_atが指定された場合は時刻に1秒足す
    elif 'end_at' in search_parameter:
        utc_time = utc_time + timedelta(seconds=RANGE_SECONDS)

    # フォーマットを整える
    utc_time = utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return utc_time


def get_device_ids(roadside_unit_id, service_location_id, device_ids, query_params):
    """
    最新の機器種別IDを取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    device_ids : array
        機器種別ID格納配列
    query_params : list
        クエリパラメータ

    Returns
    -------
    device_ids  : array
        機器種別ID格納配列
    """
    base_table_name = SENSOR_INFO_TABLE_NAME
    t_sensor_name = f"{base_table_name}_{roadside_unit_id}"

    t_sensor_info = dynamoDB.Table(t_sensor_name)

    # 機器種別IDの検索がされている場合はIDのみ返す
    if 'deviceID' in query_params:
        device_ids.append(query_params['deviceID'])
    # 機器種別IDの検索がされていない場合センサ情報から機器種別IDを取得
    else:
        index_name = 'serviceLocationID-updateTimeInfo-index'
        key_name = 'serviceLocationID'
        equal_key = int(service_location_id)
        query = {
            'IndexName': index_name,
            'KeyConditionExpression': Key(key_name).eq(equal_key),
            'ScanIndexForward': False,
            'Limit': 1
        }

        # end_atが指定された場合、指定された時間までの最新の1レコードを取得
        # end_atが指定されない場合、最新の1レコードを取得
        if 'endAt' in query_params:
            query['KeyConditionExpression'] &= Key('updateTimeInfo').lte(getTimeUtc(query_params['endAt'], 'sensor'))

        sensor_item = t_sensor_info.query(**query)

        if sensor_item['Items']:
            # 結果を代入
            sensor_item = sensor_item['Items'][0]
            sensor_attribute_info = ast.literal_eval(sensor_item.get('sensorAttributeInfo'))
            for sensor_info in sensor_attribute_info:
                device_ids.append(sensor_info['deviceID'])
            # 機器種別IDを降順にして最新の16件のみ取得
            device_ids = sorted(device_ids, reverse=True)[:MAX_DEVICE_NUM]

    return device_ids
