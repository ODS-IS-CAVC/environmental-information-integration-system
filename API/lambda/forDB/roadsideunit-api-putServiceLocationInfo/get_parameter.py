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
    parameters['attribute']['updateTimeInfo'] = str(body_data['attribute']['updateTimeInfo'])
    parameters['attribute']['formatVersion'] = int(body_data['attribute']['formatVersion'])
    parameters['attribute']['latitude'] = int(body_data['attribute']['latitude'])
    parameters['attribute']['longitude'] = int(body_data['attribute']['longitude'])
    parameters['attribute']['elevation'] = int(body_data['attribute']['elevation'])
    parameters['attribute']['approachAttributeSize'] = int(body_data['attribute']['approachAttributeSize'])
    parameters['attribute']['approachAttributeInfo'] = body_data['attribute']['approachAttributeInfo']
    parameters['attribute']['roadsideUnitList'] = body_data['attribute']['roadsideUnitList']

    return parameters
