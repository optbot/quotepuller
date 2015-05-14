"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Get active equities
===================
"""
from functools import partial
import time

from pymongo.errors import ConnectionFailure

import constants
import dbwrapper

def getequities(dbconn, logger, test_mode):
    logger.info('getting active equities')
    _retries = constants.N_DBRETRIES
    _equities = []
    while _retries > 0:
        try:
            _equities = dbwrapper.job(dbconn, logger, partial(active, test_mode))
        except ConnectionFailure:
            logger.exception('could not retrieve equities')
            _retries -= 1
            time.sleep(constants.RETRYSECS_DBCONNECT)
        else:
            _retries = 0
    return _equities

def active(test_mode, logger, client):
    # for now use production as source regardless of test_mode
    _db = client[constants.DB]
    _active = _db.equities.find({"active": True})
    _ret = [item['symbol'] for item in _active]
    logger.debug(_ret)
    return _ret
