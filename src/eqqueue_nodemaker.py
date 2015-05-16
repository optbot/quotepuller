"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Make a list of queue nodes from a list of equities
==================================================
"""

def makequeuenodes(equities, nysenow):
    """
    Create a deque containing not only the equities
    but also a timestamp for processing
    """
    return [{"symbol": _eq, "waitUntil": nysenow} for _eq in equities]
