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
import logging
from functools import partial
import signal
import sys
import os.path

import constants
import dbwrapper
import eqgetter

logger = logging.getLogger(constants.SERVICE_NAME)
test_mode = False

def stop_handler(_signal, frame):
    # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
    msg = ('SIGINT' if _signal == signal.SIGINT else 'SIGTERM')
    logger.info('signal {} received. stopping'.format(msg))
    sys.exit(0)

def run(dbconn):
    logger.info('starting')
    logger.debug('dbconn: {}'.format(dbconn))
    _equities = dbwrapper.job(dbconn, logger, partial(eqgetter.active, test_mode))
    signal.pause()

def init():
    # check for test mode
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--test', action='store_true')
    test_mode = _parser.parse_args().test
    _config = ConfigParser.SafeConfigParser()
    _sec = constants.CFGSEC_MAIN
    _config.read(constants.CONFIGFILE)
    _logpath = _config.get(_sec, 'logpath', 1) 
    _logfmt = _config.get(_sec, 'logfmt', 1)
    if test_mode:
        _logfmt += ' (TESTING)'
    _handler = logging.FileHandler(os.path.join(_logpath, 'service.log'))
    _formatter = logging.Formatter(_logfmt)
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    if test_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    dbconn = _config.get(_sec, 'dbconn', 1)
    logger.debug('dbconn: {}'.format(dbconn))
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)
    return dbconn

if __name__ == '__main__':
    _dbconn = init()
    run(_dbconn)
