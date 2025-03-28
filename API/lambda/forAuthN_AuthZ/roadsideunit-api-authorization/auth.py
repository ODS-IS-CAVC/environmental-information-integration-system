# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import logging
import uuid

import requests
from log import logger

# ログレベル設定
logger.setLevel(logging.INFO)


def token_introspection(url, data_distribution_api_key, access_token):
    """
    トークンイントロスペクション
    Parameters
    ----------
    url : string
        API URL
    data_distribution_api_key : string
        データ流通層用APIキー
    access_token : string
        アクセストークン

    Returns
    -------
    res_body : dict
        レスポンスボディ
    """
    try:
        UUID = str(uuid.uuid4())
        headers = {
            'apiKey': data_distribution_api_key,
            'X-Tracking': UUID,
            'Content-Type': 'application/json'
        }
        body = {'idToken': access_token}
        res = requests.request(
            'POST',
            url,
            headers=headers,
            json=body
        )

        # status_codeが400-599の時に HTTPError を raise
        res.raise_for_status()

        res_body = res.json()
        return True if res_body['active'] else False

    except requests.exceptions.HTTPError as he:
        logger.error(he)
        logger.error(he.response.text)
        return False
    except Exception as e:
        logger.error(e)
        return False
