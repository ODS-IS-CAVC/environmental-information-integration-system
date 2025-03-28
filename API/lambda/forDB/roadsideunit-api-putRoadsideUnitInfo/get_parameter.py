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
    parameters['attribute']['roadsideUnitName'] = str(body_data['attribute']['roadsideUnitName'])
    parameters['attribute']['productNumber'] = str(body_data['attribute']['productNumber'])
    if 'manufacturer' in body_data['attribute']:
        parameters['attribute']['manufacturer'] = str(body_data['attribute']['manufacturer'])
    if 'customer' in body_data['attribute']:
        parameters['attribute']['customer'] = str(body_data['attribute']['customer'])
    parameters['attribute']['licensingInfo'] = str(body_data['attribute']['licensingInfo'])
    parameters['attribute']['initialRegistrationDate'] = str(body_data['attribute']['initialRegistrationDate'])
    parameters['attribute']['powerConsumption'] = int(body_data['attribute']['powerConsumption'])
    parameters['attribute']['grossWeight'] = int(body_data['attribute']['grossWeight'])
    parameters['attribute']['materialType'] = int(body_data['attribute']['materialType'])
    parameters['attribute']['dateOfInstallation'] = str(body_data['attribute']['dateOfInstallation'])
    parameters['attribute']['latitude'] = int(body_data['attribute']['latitude'])
    parameters['attribute']['longitude'] = int(body_data['attribute']['longitude'])
    parameters['attribute']['roadsideUnitManager'] = str(body_data['attribute']['roadsideUnitManager'])
    parameters['attribute']['installationSiteManager'] = str(body_data['attribute']['installationSiteManager'])
    parameters['attribute']['lastInspectionDate'] = str(body_data['attribute']['lastInspectionDate'])
    parameters['attribute']['nextInspectionDate'] = str(body_data['attribute']['nextInspectionDate'])

    return parameters
