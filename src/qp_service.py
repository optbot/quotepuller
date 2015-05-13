"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Manage quote retrieval (:mod:`optbot.quote_mediator`)
=====================================================

.. currentmodule:: optbot.quote_mediator
"""

import datetime as dt
import time

from pandas.tseries.offsets import BDay
from pymongo.errors import ConnectionFailure
from pytz import timezone

import constants

class QpService(object):
    def __init__(self, logger, test_mode):
        self._test_mode = test_mode
        self._logger = logger
        self._job = None
        self._secstoretry = constants.RETRYSECS_QUOTES
        self._running = False
        # for more accurate logging of shutdown
        self._jobinprogress = False
        self._logger.debug('quote mediator created')

    def run(self):
        while self._running:
            # if db isn't available, wait and try again
            try:
                if test_mode:
                    self._run_test()
                else:
                    self._run_live()
            except ConnectionFailure:
                self._logger.exception('db unavailable')
                time.sleep(constants.RETRY_DBCONNECT)
            else:
                break

    def _run_test(self):
        self._logger.debug('running in test mode')
        pass

    def _run_live(self):
        self._jobinprogress = True
        _now = dt.datetime.now(tz=timezone('US/Eastern'))
        _mktday = ismktopen(_now)
        if not _mktday and not run_any_day:
            self._logger.info("Market not open today: {}".format(_now))
            self._secstoretry = _secstowait(_now)
        elif _now.hour < 16 and _mktday:
            self._logger.info("Today's closes unavailable at {}".format(_now))
            self._secstoretry = _secstowait(_now, True)
        elif conn.job(partial(updateall, _now), self._logger):
            self._logger.info("Successful retrieval at {}".format(_now))
            self._secstoretry = _secstowait(_now)
        else:
            self._logger.info("Retrieval failed at {}".format(_now))
            self._secstoretry = constants.RETRYSECS_QUOTES
        if self._running:
            self._logger.info("Retrying in {:.1f} hours".format(self._secstoretry / (60. * 60.)))
            self._job = threading.Timer(self._secstoretry, self.run)
            self._job.start()
        else:
            # this should be the case when job is cancelled while in progress
            self._logger.info("quote mediator stopped after task completed")
        self._jobinprogress = False

    def start(self):
        self._logger.info("starting")
        self._running = True
        self.run()

    def close(self):
        self._logger.info("stopping")
        self._running = False
        if self._job is not None:
            self._job.cancel()
        if not self._jobinprogress:
            self._logger.info("quote mediator stopped, next run canceled")


def ismktopen(date):
    return date.day == ((date + BDay()) - BDay()).day

def _secstowait(curr_est, againtoday=False):
    if againtoday:
        if curr_est.hour < 16:
            _nextclose = curr_est.replace(hour=16, minute=15)
            return (_nextclose - curr_est).total_seconds()
        return _constants.RETRYSECS_QUOTES
    _nextbday = curr_est + BDay()
    _nextclose = _nextbday.replace(hour=16, minute=15)
    return (_nextclose - curr_est).total_seconds()

def updateeq(db, eq, nysenow):
    _quotes = db[_constants.QUOTES]
    # PyMongo mistakenly interprets the value of 'Quote_Time' as UTC rather than EST
    # So we need to offset by at least 5 hours.
    # The following checks for any stored value from today regardless of quote time.
    _today = nysenow.replace(hour=3)
    if _quotes.find_one({'Underlying': {'$in': [eq.lower(), eq.upper()]}, 'Quote_Time': {'$gte': _today}}) is not None:
        logger.warn("{} quotes for '{}' already inserted.".format(nysenow.strftime('%Y-%m-%d'), eq)) 
        return True
    logger.info("Downloading options quotes for '{}'".format(eq))
    try:
        _opts = pn.opt.get(eq)
        _entries = map(partial(utils.fixentry, nysenow), _opts.tolist())
        if len(_entries) == 0:
            logger.info("Empty list returned for '{}'".format(eq))
            return False
        _bulk = _quotes.initialize_unordered_bulk_op()
        logger.info("Inserting quotes for '{}' into '{}'".format(eq, _constants.QUOTES))
        for _entry in _entries:
            _bulk.insert(_entry)
            logger.debug("{} queued for insert into {}.{}".format(_entry, _constants.DB, _constants.QUOTES))
        try:
            _result = _bulk.execute()
        except BulkWriteError:
            logger.exception("Error writing to database")
            return False
        else:
            logger.info("{} records inserted into {}.{}".format(_result['nInserted'], _constants.DB, _constants.QUOTES))
            return True
    except pd.io.data.RemoteDataError:
        logger.exception("exception retrieving quotes for '{}'".format(eq))
        return False
    except:
        logger.exception("unknown exception")
        return False

def updateall(nysenow, client):
    _db = client[_constants.DB]
    _active = _db[_constants.ACTIVE]
    _success = True
    for _eq in _active.find():
        _success = updateeq(_db, _eq['equity'], nysenow) and _success
    return _success
