# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging
from datetime import datetime

from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def get_body(body):
    """
    body 要素取得
    Returns
    -------
    parameters  : Array
        グループ名
    """

    body_data = json.loads(body)

    parameters = {}
    # パラメータを代入
    if 'dataModelType' in body_data:
        parameters['dataModelType'] = str(body_data['dataModelType'])
    parameters['attribute'] = {}
    parameters['attribute']['time_minutes'] = getTimeMinutes(body_data['attribute']['updateTimeInfo'])
    parameters['attribute']['updateTimeInfo'] = str(body_data['attribute']['updateTimeInfo'])
    parameters['attribute']['serviceLocationID'] = int(body_data['attribute']['serviceLocationID'])
    parameters['attribute']['roadsideUnitID'] = int(body_data['attribute']['roadsideUnitID'])
    parameters['attribute']['formatVersion'] = int(body_data['attribute']['formatVersion'])
    parameters['attribute']['operationClassificationCode'] = int(body_data['attribute']['operationClassificationCode'])
    parameters['attribute']['serviceAvailability'] = int(body_data['attribute']['serviceAvailability'])
    parameters['attribute']['deviceClassificationNum'] = int(body_data['attribute']['deviceClassificationNum'])
    parameters['attribute']['deviceClassificationAliveInfo'] = body_data['attribute']['deviceClassificationAliveInfo']

    return parameters


def getTimeMinutes(updateTimeInfo):
    """
    分までの更新時刻情報取得
    Parameters
    -------
    updateTimeInfo : String
        更新時刻情報

    Returns
    -------
    format_update_time : String
        更新時刻情報（分まで）
    """
    update_time = datetime.strptime(updateTimeInfo, '%Y-%m-%dT%H:%M:%S.%f%z')
    # 時刻を「分」までのフォーマットで取得
    format_update_time = update_time.strftime('%Y-%m-%d %H:%M')

    return format_update_time
