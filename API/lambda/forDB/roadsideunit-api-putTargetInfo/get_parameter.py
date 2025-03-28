import json
import logging

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
    parameters['attribute']['roadsideUnitID'] = int(body_data['attribute']['roadsideUnitID'])
    parameters['attribute']['serviceLocationID'] = int(body_data['attribute']['serviceLocationID'])
    parameters['attribute']['updateTimeInfo'] = str(body_data['attribute']['updateTimeInfo'])
    parameters['attribute']['formatVersion'] = int(body_data['attribute']['formatVersion'])
    parameters['attribute']['deviceIndividualInfo'] = body_data['attribute']['deviceIndividualInfo']

    return parameters
