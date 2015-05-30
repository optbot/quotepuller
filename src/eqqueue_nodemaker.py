"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Make a list of queue nodes from a list of equities
==================================================
"""
import datetime as dt

def makequeuenodes(equities, nysenow, test_mode):
    """
    Create a deque containing not only the equities
    but also a timestamp for processing
    """
    _wait_until = nysenow
    if test_mode:
        _wait_until = nysenow + dt.timedelta(seconds=10)
    return [{"symbol": _eq, "waitUntil": _wait_until} for _eq in equities]
