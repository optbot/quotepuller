"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Time to wait until next run
===========================
"""

from pandas.tseries.offsets import BDay
from pytz import timezone

def secs_to_next_run(logger):
    logger.info('determining correct wait time')
    return 0.
