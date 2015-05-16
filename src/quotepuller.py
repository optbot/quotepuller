"""
.. Copyright (c) 2015 Marshall Farrier, Robert Rodrigues, Mark Scappini
   license http://opensource.org/licenses/MIT

Quote puller service main
=========================
Start the service from the python interpreter in the appropriate virtual
environment:
http://stackoverflow.com/questions/7807315/daemonizing-a-python-script-in-debian-using-virtualenv
For example:

    $ /var/local/.virtualenvs/quotepuller/bin/python <path>/quotepuller.py
"""
import argparse
import ConfigParser
from collections import deque
import datetime as dt
import logging
import os.path
import signal
import sys

from pytz import timezone

import constants
from eqgetter import getequities
from eqqueue_nodemaker import makequeuenodes
from qp_runner import savequotes

class QuotePuller(object):
    def __init__(self):
        """
        Members:
        dbconn
        equities
        logger
        service
        test_mode
        """
        _parser = argparse.ArgumentParser()
        _parser.add_argument('--test', action='store_true')
        self.test_mode = _parser.parse_args().test
        _config = ConfigParser.SafeConfigParser()
        _section = constants.CFGSECTION_MAIN
        _config.read(constants.CONFIGFILE)
        # set up logging
        self.logger = logging.getLogger(constants.SERVICE_NAME)
        _logpath = _config.get(_section, 'logpath', 1) 
        _logfmt = _config.get(_section, 'logfmt', 1)
        if self.test_mode:
            _logfmt += ' (TESTING)'
        _handler = logging.FileHandler(os.path.join(_logpath, 'service.log'))
        _formatter = logging.Formatter(_logfmt)
        _handler.setFormatter(_formatter)
        self.logger.addHandler(_handler)
        if self.test_mode:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.dbconn = _config.get(_section, 'dbconn', 1)
        self.logger.debug('dbconn: {}'.format(self.dbconn))
        self.equities = deque()
        signal.signal(signal.SIGTERM, self.stop_handler)
        signal.signal(signal.SIGINT, self.stop_handler)

    def run(self):
        self.logger.info('starting')
        _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
        self.logger.info('time in NY is {}'.format(_nysenow))
        _equities = getequities(self.dbconn, self.logger, self.test_mode)
        _eqnodes = makequeuenodes(_equities, _nysenow)
        for _node in _eqnodes:
            self.equities.append(_node)
        self.logger.debug(self.equities)
        try:
            self.process_queue()
        except:
            self.logger.exception('something went wrong')
        signal.pause()

    def process_queue(self):
        _retrysecs = (constants.RETRYSECS_QUOTES_TST if self.test_mode else
                constants.RETRYSECS_QUOTES)
        self.logger.info('retry seconds set to {}'.format(_retrysecs))
        while self.equities:
            _eq = self.equities.pop()['symbol']
            if not savequotes(self.dbconn, self.logger, self.test_mode, _eq):
                _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
                _wait_until = _nysenow + dt.timedelta(0, _retrysecs)
                self.equities.appendleft({"symbol": _eq, "waitUntil": _wait_until})

    def stop_handler(self, sig, frame):
        # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
        msg = ('SIGINT' if sig == signal.SIGINT else 'SIGTERM')
        self.logger.info('signal {} received. stopping'.format(msg))
        sys.exit(0)

if __name__ == '__main__':
    QuotePuller().run()
