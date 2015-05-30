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
from pymongo.errors import BulkWriteError
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
    _dbname = _get_dbname(logger, test_mode)
    _success = False
    # see if quotes for today are already present
    try:
        if dbwrapper.job(dbconn, logger, partial(_already_saved, equity, _nysenow, _dbname)):
            if not test_mode:
                return True
            logger.debug('entries found for {}, continuing in test mode'.format(equity))
    except ConnectionFailure:
        logger.exception("could not connect to mongo")
        return False
    # get today's quotes
    try:
        _opts = pn.opt.get(equity)
        logger.info('fixing timestamps')
        _entries = map(partial(_fixentry, _nysenow), _opts.tolist())
        if len(_entries) == 0:
            logger.info("empty list returned for '{}'".format(equity))
            return True
    except ValueError:
        logger.exception("no options for equity '{}'".format(equity))
        return True
    except:
        logger.exception("exception retrieving quotes for '{}'".format(equity))
        return False
    logger.info("quotes retrieved for equity '{}'".format(equity))
    # push to mongo
    try:
        logger.info("pushing quote data for {} to mongo".format(equity))
        _success = dbwrapper.job(dbconn, logger, partial(_save, _dbname, _entries,))
    except ConnectionFailure:
        logger.exception("could not connect to mongo")
        return False
    except:
        logger.exception("exception pushing quotes for '{}' to mongo".format(equity))
        return False
    return _success

def _save(dbname, entries, logger, dbclient):
    _db = dbclient[dbname]
    _quotes = _db[constants.QUOTES]
    logger.info('inserting quotes into {}.{}'.format(dbname, constants.QUOTES))
    _bulk = _quotes.initialize_unordered_bulk_op()
    for _entry in entries:
        _bulk.insert(_entry)
        logger.debug("{} queued for insertion".format(_entry))
    try:
        _result = _bulk.execute()
    except BulkWriteError:
        logger.exception("error writing to database")
        return False
    else:
        logger.info("{} records inserted".format(_result['nInserted']))
        return True

def _already_saved(equity, nysenow, dbname, logger, dbclient):
    # PyMongo mistakenly interprets the value of 'Quote_Time' as UTC rather than EST
    # So we need to offset by at least 5 hours.
    # The following checks for any stored value from today regardless of quote time.
    _today = nysenow.replace(hour=3)
    _db = dbclient[dbname]
    _quotes = _db[constants.QUOTES]
    if _quotes.find_one({'Underlying': equity, 'Quote_Time': {'$gte': _today}}) is not None:
        logger.warn("{} quotes for '{}' already inserted.".format(nysenow.strftime('%Y-%m-%d'), equity)) 
        return True
    logger.debug("quotes for '{}' not yet saved".format(equity))
    return False

def _get_dbname(logger, test_mode):
    _dbname = constants.DB
    logger.info('using db {}'.format(_dbname))
    if test_mode:
        _dbname = constants.DB_TEST
        logger.info('db name overridden in test mode')
        logger.info('using db {}'.format(_dbname))
    return _dbname

def _fixentry(nysenow, entry):
    _fixed = entry
    _quotetime = ((nysenow + BDay()) - BDay()).to_datetime().replace(hour=entry['Quote_Time'].hour, 
            minute=entry['Quote_Time'].minute, second=entry['Quote_Time'].second)
    _fixed['Quote_Time'] = _quotetime
    _fixed['Expiry'] = entry['Expiry'].replace(tzinfo=timezone('US/Eastern'))
    return _fixed 
