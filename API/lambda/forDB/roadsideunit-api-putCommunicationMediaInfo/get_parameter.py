# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import json
import logging

from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def get_body(body):
    """
    event body 要素取得
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
    parameters['attribute']['serviceLocationID'] = int(body_data['attribute']['serviceLocationID'])
    parameters['attribute']['roadsideUnitID'] = int(body_data['attribute']['roadsideUnitID'])
    parameters['attribute']['updateTimeInfo'] = str(body_data['attribute']['updateTimeInfo'])
    parameters['attribute']['formatVersion'] = int(body_data['attribute']['formatVersion'])
    parameters['attribute']['communicationMediaNum'] = int(body_data['attribute']['communicationMediaNum'])
    parameters['attribute']['communicationMediaIDs'] = body_data['attribute']['communicationMediaIDs']

    return parameters
