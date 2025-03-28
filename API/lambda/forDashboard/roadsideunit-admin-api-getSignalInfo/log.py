# Copyright 2024 Smart Mobility Infrastructure Collaborative Innovation Partnership. All rights reserved.

import sys
import logging


"""
フォーマット設定済みロガー
"""
logger = logging.getLogger()
[logger.removeHandler(h) for h in logger.handlers]
log_format = '[%(levelname)s][%(filename)s][%(funcName)s:%(lineno)d]\t%(message)s'
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(stdout_handler)
logger