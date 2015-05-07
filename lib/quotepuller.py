"""
.. Copyright (c) 2015 Marshall Farrier, Robert Rodrigues, Mark Scappini
   license http://opensource.org/licenses/MIT

Quote puller service main
=========================
"""
import ConfigParser
import logging
import signal
import sys

import constants

logger = logging.getLogger(constants.SERVICE_NAME)

def stop_handler(_signal, frame):
    # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
    msg = ('SIGINT' if _signal == signal.SIGINT else 'SIGTERM')
    logger.info('signal {} received. stopping'.format(msg))
    sys.exit(0)

def run():
    logger.info('starting')
    signal.pause()

def init():
    _config = ConfigParser.SafeConfigParser()
    _sec = constants.CFGSEC_MAIN
    _config.read(constants.CONFIGFILE)
    _logpath = _config.get(_sec, 'logpath', 1) 
    _logfmt = _config.get(_sec, 'logfmt', 1)
    _dbconn = _config.get(_sec, 'dbconn', 1)
    print(_logpath)
    print(_logfmt)
    print(_dbconn)
    return
    _handler = logging.FileHandler(_logpath)
    _formatter = logging.Formatter(_logfmt)
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)

if __name__ == '__main__':
    init()
    run()
