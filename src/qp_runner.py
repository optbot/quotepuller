"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Manage quote retrieval (:mod:`optbot.qp_service`)
=====================================================

.. currentmodule:: optbot.qp_service
"""

import datetime as dt
from functools import partial
import time

from pandas.tseries.offsets import BDay
from pymongo.errors import ConnectionFailure
import pynance as pn
from pytz import timezone

import constants
import dbwrapper

def savequotes(dbconn, logger, test_mode, equity):
    """
    Return true if operation successful, otherwise false
    """
    logger.info("retrieving options quotes for '{}'".format(equity))
    _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
    try:
        _opts = pn.opt.get(equity)
    except ValueError:
        logger.exception("no options for equity '{}'".format(equity))
        return True
    except:
        logger.exception("exception retrieving quotes for '{}'".format(equity))
        return False
    logger.info("quotes retrieved for equity '{}'".format(equity))
    try:
        logger.info("pushing quote data for {} to mongo".format(equity))
        dbwrapper.job(dbconn, logger, partial(_save, _opts, _nysenow, test_mode))
    except ConnectionFailure:
        logger.exception("could not connect to mongo")
        return False
    except:
        logger.exception("exception pushing quotes for '{}' to mongo".format(equity))
        return False
    return True

def _save(opt_quotes, nysenow, test_mode, logger, dbclient):
    logger.info('fixing timestamps')
    _entries = map(partial(_fixentry, nysenow), opt_quotes.tolist())
    if test_mode:
        logger.debug('test mode')
    else:
        logger.info('live mode')

def _fixentry(nysenow, entry):
    _fixed = entry
    _quotetime = ((nysenow + BDay()) - BDay()).to_datetime().replace(hour=entry['Quote_Time'].hour, 
            minute=entry['Quote_Time'].minute, second=entry['Quote_Time'].second)
    _fixed['Quote_Time'] = _quotetime
    _fixed['Expiry'] = entry['Expiry'].replace(tzinfo=timezone('US/Eastern'))
    return _fixed 
