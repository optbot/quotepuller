"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Manage quote retrieval (:mod:`optbot.qp_service`)
=====================================================

.. currentmodule:: optbot.qp_service
"""

import datetime as dt
import time

from pandas.tseries.offsets import BDay
from pymongo.errors import ConnectionFailure
from pytz import timezone

import constants

class QpService(object):
    def __init__(self, logger, test_mode):
        self.test_mode = test_mode
        self.logger = logger
        self.job = None
        self.secstoretry = constants.RETRYSECS_QUOTES
        self.running = False
        # for more accurate logging of shutdown
        self.jobinprogress = False
        self.logger.debug('qp service created')
