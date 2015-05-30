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
import threading
import time

from pytz import timezone

import constants
from eqgetter import getequities
from eqqueue_nodemaker import makequeuenodes
from qp_runner import savequotes
from timing_mgr import secs_to_next_run

class QuotePuller(object):
    def __init__(self):
        """
        Members:
        dbconn
        equities
        logger
        service
        test_mode
        _quote_retrysecs
        _die
        _job
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
        self._quote_retrysecs = (constants.RETRYSECS_QUOTES_TST if self.test_mode else
                constants.RETRYSECS_QUOTES)
        self.logger.info('retry seconds set to {}'.format(self._quote_retrysecs))
        self._die = False
        self._job = None
        self._set_secs_to_next_run(True)
        signal.signal(signal.SIGTERM, self.stop_handler)
        signal.signal(signal.SIGINT, self.stop_handler)

    def start(self):
        self.logger.info('starting')
        self._setup_nextjob()
        signal.pause()

    def run(self):
        self.logger.info('running')
        try:
            _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
            self.logger.info('time in NY is {}'.format(_nysenow))
            _equities = getequities(self.dbconn, self.logger, self.test_mode)
            _eqnodes = makequeuenodes(_equities, _nysenow, self.test_mode)
            for _node in _eqnodes:
                self.equities.append(_node)
            self.logger.debug(self.equities)
            self._process_queue()
        except SystemExit:
            self.logger.info('terminating process')
            sys.exit(0)
        except:
            self.logger.exception('unknown exception')
            raise
        self._set_secs_to_next_run(False)
        self._setup_nextjob()

    def _setup_nextjob(self):
        self._job = threading.Timer(self._secs_to_next_run, self.run)
        self._job.start()
        self.logger.info('job set to start in {:.0f} seconds'.format(self._secs_to_next_run))

    def _set_secs_to_next_run(self, runtoday):
        self._secs_to_next_run = secs_to_next_run(self.logger, runtoday)
        if self.test_mode:
            _test_delay_secs = 2.
            self.logger.debug('resetting delay to {} in test mode'.format(_test_delay_secs))
            self._secs_to_next_run = _test_delay_secs

    def _process_queue(self):
        _counter = 0
        _autofail_tst = 5
        while self.equities:
            _queue_node = self.equities.pop()
            _wait_to_process(self.logger, _queue_node)
            _eq = _queue_node['symbol']
            if not savequotes(self.dbconn, self.logger, self.test_mode, _eq):
                self._requeue(_eq)
            if self.test_mode and _counter == _autofail_tst:
                self.logger.debug('simulating failure for testing')
                self._requeue(_eq)
            _counter += 1
            if self._die:
                self.logger.info("dying during or after pulling quotes for '{}'".format(_eq))
                raise SystemExit

    def _requeue(self, _eq):
        _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
        _wait_until = _nysenow + dt.timedelta(0, self._quote_retrysecs)
        self.equities.appendleft({"symbol": _eq, "waitUntil": _wait_until})
        self.logger.debug(self.equities)

    def stop_handler(self, sig, frame):
        # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
        msg = ('SIGINT' if sig == signal.SIGINT else 'SIGTERM')
        self.logger.info('signal {} received. stopping'.format(msg))
        self._die = True
        self._job.cancel()
        sys.exit(0)
    
def _wait_to_process(logger, queue_node):
    _nysenow = dt.datetime.now(tz=timezone('US/Eastern'))
    _wait_until = queue_node['waitUntil']
    if _nysenow < _wait_until:
        _secs_to_wait = (_wait_until - _nysenow).total_seconds()
        logger.info("item not ready for processing. waiting {} seconds".format(_secs_to_wait))
        time.sleep(_secs_to_wait)
    return

if __name__ == '__main__':
    QuotePuller().start()
