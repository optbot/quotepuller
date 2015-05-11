"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Get active equities
===================
"""

import constants

def active(test_mode, logger, client):
    # for now use production as source regardless of test_mode
    _db = client[constants.DB]
    _active = _db.equities.find({"active": True})
    _ret = [item['symbol'] for item in _active]
    logger.debug(_ret)
    return _ret
