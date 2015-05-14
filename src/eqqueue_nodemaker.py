"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Make a list of queue nodes from a list of equities
==================================================
"""
import datetime as dt

from pytz import timezone

def makequeuenodes(equities):
    """
    Create a deque containing not only the equities
    but also a timestamp for processing
    """
    _now = dt.datetime.now(tz=timezone('US/Eastern'))
    return [{"symbol": _eq, "waitUntil": _now} for _eq in equities]
