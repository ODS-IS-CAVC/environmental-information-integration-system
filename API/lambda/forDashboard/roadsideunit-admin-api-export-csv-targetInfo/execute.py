# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import ast
import csv
import logging
from datetime import datetime, timedelta

import awswrangler as wr
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)

# DynamoDBオブジェクト
dynamoDB = boto3.resource('dynamodb')
Key = boto3.dynamodb.conditions.Key


def get_data(query_params, target_info_table_name, sensor_info_table_name):
    """
    物標情報取得
    Parameters
    ----------
    query_params : list
        クエリパラメータ
    target_info_table_name : string
        物標情報テーブル名
    sensor_info_table_name : string
        センサ情報テーブル名

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
        data_list, response_status = get_data_execute(query_params, response_status, target_info_table_name, sensor_info_table_name)

    except Exception:
        logger.error('other error')
        raise

    return data_list, response_status


def get_data_execute(query_params, response_status, target_info_table_name, sensor_info_table_name):
    """
    物標情報取得
    Parameters
    ----------
    query_params : list
        クエリパラメータ
    response_status : int
        ステータスコード
    target_info_table_name : string
        物標情報テーブル名
    sensor_info_table_name : string
        センサ情報テーブル名

    Returns
    -------
    result : Array
        取得されたデータ
    response_status : 200:正常終了 204:データ未取得
    """

    # 取得する物標情報テーブル名を作成
    t_target_name = f"{target_info_table_name}_{query_params['roadsideUnitID']}_{query_params['serviceLocationID']}"
    # テーブル情報を取得
    t_target_info = dynamoDB.Table(t_target_name)

    # 物標情報を整形し、取得
    result, response_status = get_target_value(query_params['roadsideUnitID'], query_params['serviceLocationID'], t_target_info, sensor_info_table_name, response_status, query_params)

    return result, response_status


def get_target_value(roadside_unit_id, service_location_id, t_target_info, sensor_info_table_name, response_status, query_params):
    """
    物標情報を整形し、取得
    Parameters
    ----------
    roadside_unit_id : int
        路側機ID
    service_location_id : int
        サービス地点情報ID
    t_target_info : string
        物標情報テーブル
    sensor_info_table_name : string
        センサ情報テーブル名
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

    result = []
    device_ids = []

    # クエリの実行
    device_ids = get_device_ids(roadside_unit_id, service_location_id, device_ids, query_params, sensor_info_table_name)
    logger.info(device_ids)
    if len(device_ids) != 0:
        for device_id in device_ids:
            # クエリの取得
            target_query = get_query_items(query_params, device_id)
            # クエリの実行
            try:
                response = t_target_info.query(**target_query)
                # logger.info(response)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    response_status = 204
                    return result, response_status
            result.extend(response.get('Items', []))
    if not result:
        response_status = 204
        return result, response_status

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

    # クエリ作成
    query = {
       'IndexName': 'deviceID-time_utc-index',
       'KeyConditionExpression': Key('deviceID').eq(int(device_id)),
       'Limit': 255
    }

    # データ取得開始時刻を取得
    start_date = datetime.strptime(query_params['startAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # データ取得期間を加算した時刻を取得
    period_date = start_date + timedelta(seconds=int(query_params['period']))
    # 新しい日付をフォーマット
    format_date = period_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

    # 指定された範囲の時間から、古い順に取得する
    query['KeyConditionExpression'] &= Key('time_utc').between(query_params['startAt'], format_date)
    query['ScanIndexForward'] = True

    return query


def get_device_ids(roadside_unit_id, service_location_id, device_ids, query_params, sensor_info_table_name):
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
    sensor_info_table_name : string
        センサ情報テーブル名

    Returns
    -------
    device_ids  : array
        機器種別ID格納配列
    """
    base_table_name = sensor_info_table_name
    t_sensor_name = f"{base_table_name}_{roadside_unit_id}"

    t_sensor_info = dynamoDB.Table(t_sensor_name)

    # センサ情報から機器種別IDを取得
    index_name = 'serviceLocationID-updateTimeInfo-index'
    key_name = 'serviceLocationID'
    equal_key = int(service_location_id)
    query = {
        'IndexName': index_name,
        'KeyConditionExpression': Key(key_name).eq(equal_key),
        'ScanIndexForward': False,
        'Limit': 1
    }

    sensor_item = t_sensor_info.query(**query)

    if sensor_item['Items']:
        # 結果を代入
        sensor_item = sensor_item['Items'][0]
        sensor_attribute_info = ast.literal_eval(sensor_item.get('sensorAttributeInfo'))
        for sensor_info in sensor_attribute_info:
            device_ids.append(sensor_info['deviceID'])
        # 機器種別IDを降順にして最新の16件のみ取得
        device_ids = sorted(device_ids, reverse=True)[:16]

    return device_ids


def data_format(data, query_params, target_info_bucket_name, target_info_table_name, region_name):
    """
    物標情報を整形する
    Parameters
    ----------
    data : Array
        指定した範囲の物標情報
    query_params : list
        クエリパラメータ
    target_info_bucket_name : str
        格納するs3バケット名
    target_info_table_name : string
        物標情報テーブル名
    region_name : str
        リージョン名

    Returns
    -------
    result : dict
        s3バケットへのパス
    """

    # 取得データをDataFrame化
    df = pd.DataFrame(data)

    # 不要なカラムを削除
    df = df.drop(columns=['time_minutes', 'time_utc', 'unique_time'])

    # columnを仕様書に合わせて並び替え
    df = df.reindex(columns=['dataModelType', 'serviceLocationID', 'roadsideUnitID', 'updateTimeInfo', 'formatVersion', 'deviceID', 'targetIndividualInfo'])

    # 'targetIndividualInfo'列を辞書として展開
    target_info = df['targetIndividualInfo'].apply(ast.literal_eval).apply(pd.Series)

    # 元のDataFrameに展開したカラムを結合
    df = pd.concat([df.drop(columns='targetIndividualInfo'), target_info], axis=1)

    # deviceIDの出現回数をカウントし、元のDataFrameにマージ
    device_counts = df['deviceID'].value_counts().reset_index()
    device_counts.columns = ['deviceID', 'deviceNum']
    df = df.merge(device_counts, on='deviceID', how='left')

    # deviceNumを仕様書の位置に並び替え
    cols = df.columns.tolist()
    cols.remove('deviceNum')
    cols.insert(5, 'deviceNum')
    df = df[cols]

    # targetIDの出現回数をカウントし、元のDataFrameにマージ
    device_counts = df['targetID'].value_counts().reset_index()
    device_counts.columns = ['targetID', 'targetNum']
    df = df.merge(device_counts, on='targetID', how='left')

    # targetNumを仕様書の位置に並び替え
    cols = df.columns.tolist()
    cols.remove('targetNum')
    cols.insert(7, 'targetNum')
    df = df[cols]

    # s3にアップロード
    result = export_csv(df, query_params, target_info_bucket_name, target_info_table_name, region_name)

    return result


def export_csv(df, query_params, target_info_bucket_name, target_info_table_name, region_name):
    """
    csv出力し、s3バケットに格納
    Parameters
    ----------
    df : DataFrame
        整形済データ
    query_params : list
        クエリパラメータ
    target_info_bucket_name : str
        格納するs3バケット名
    target_info_table_name : string
        物標情報テーブル名
    region_name : str
        リージョン名

    Returns
    -------
    result : dict
        s3バケットへのパス
    """
    # データ取得開始時刻を取得
    start_date = datetime.strptime(query_params['startAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # データ取得期間を加算した時刻を取得
    period_date = start_date + timedelta(seconds=int(query_params['period']))

    # CSVファイル名の日時を整形
    start_year_mon_day = f"{start_date.year}{start_date.month:02d}{start_date.day:02d}"
    start_hour_min_sec = f"{start_date.hour}{start_date.minute:02d}{start_date.second:02d}"
    period_hour_min_sec = f"{period_date.hour}{period_date.minute:02d}{period_date.second:02d}"

    # CSVファイル名を定義
    target_info_file_name = 'target-info' + '-' + str(query_params['roadsideUnitID']) + '-' + str(query_params['serviceLocationID']) + '-' + start_year_mon_day + '-' + start_hour_min_sec + '-' + period_hour_min_sec + '.csv'

    # 出力するS3バケットへのパスを定義
    s3_path = f's3://{target_info_bucket_name}/{target_info_table_name}/{target_info_file_name}'

    # s3にデータを出力
    wr.s3.to_csv(
        df=df,
        path=s3_path,
        index=False,
        quoting=csv.QUOTE_ALL
    )

    # 作成したCSVファイルへのURLを作成
    target_info_url = f"https://{region_name}.console.aws.amazon.com/s3/buckets/{target_info_bucket_name}?prefix={target_info_table_name}/"

    # URLを辞書型で定義
    result = {
        "s3_bucket_url": target_info_url
    }

    return result
