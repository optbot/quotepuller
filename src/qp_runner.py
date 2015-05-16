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

def savequotes(dbconn, logger, test_mode, equity):
    """
    Return true if operation successful, otherwise false
    """
    logger.info("retrieving options quotes for '{}'".format(equity))
    return True

def _fixentry(nysenow, entry):
    _fixed = entry
    _quotetime = ((nysenow + BDay()) - BDay()).to_datetime().replace(hour=entry['Quote_Time'].hour, 
            minute=entry['Quote_Time'].minute, second=entry['Quote_Time'].second)
    _fixed['Quote_Time'] = _quotetime
    _fixed['Expiry'] = entry['Expiry'].replace(tzinfo=timezone('US/Eastern'))
    return _fixed 
