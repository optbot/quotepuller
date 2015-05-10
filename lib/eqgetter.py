"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Get active equities
===================
"""

import dbconn
import constants

def active(logger, test_mode, client):
    # for now use production as source regardless of test_mode
    _db = client[constants.DB]
    _active = _db.find({"active": True})
    return [item['symbol'] for item in _active]

