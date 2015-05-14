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
import logging
import os.path
import signal
import sys

import constants
import eqgetter
from eqgetter import getequities
from eqqueue_nodemaker import makequeuenodes
from qp_service import QpService

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
        self.service = QpService(self.logger, self.test_mode)
        signal.signal(signal.SIGTERM, self.stop_handler)
        signal.signal(signal.SIGINT, self.stop_handler)

    def run(self):
        self.logger.info('starting')
        _equities = getequities(self.dbconn, self.logger, self.test_mode)
        _eqnodes = makequeuenodes(_equities)
        for _node in _eqnodes:
            self.equities.append(_node)
        self.logger.debug(self.equities)
        signal.pause()

    def stop_handler(self, sig, frame):
        # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
        msg = ('SIGINT' if sig == signal.SIGINT else 'SIGTERM')
        self.logger.info('signal {} received. stopping'.format(msg))
        sys.exit(0)

if __name__ == '__main__':
    QuotePuller().run()
