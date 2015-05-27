"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Time to wait until next run
===========================
"""
import datetime as dt

from pandas.tseries.offsets import BDay
from pytz import timezone

def secs_to_next_run(logger, runtoday):
    logger.info('determining wait time')
    _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
    # wait a few seconds for mongo to start
    _ret = 15.
    if runtoday and _nysenow.hour >= 16 and _ismktopen(_nysenow):
        logger.info('starting immediately on business day after market close')
        return _ret
    _nextclose = _getnextclose(logger, _nysenow)
    _ret = (_nextclose - _nysenow).total_seconds()
    if _ret < 60. * 6.:
        logger.info("next run in {:.0f} seconds".format(_ret))
    else:
        logger.info("next run in {:.1f} hours".format(_ret / (60. * 60.)))
    return _ret

def _getnextclose(logger, nysenow):
    if nysenow.hour < 16:
        logger.info('waiting for market to close today')
        return nysenow.replace(hour=16, minute=15)
    logger.info('waiting for market close on next business day')
    return (nysenow + BDay()).replace(hour=16, minute=15)

def _ismktopen(date):
    return date.day == ((date + BDay()) - BDay()).day
