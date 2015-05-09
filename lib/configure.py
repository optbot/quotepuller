"""
.. Copyright (c) 2015 Marshall Farrier, Robert Rodrigues, Mark Scappini
   license http://opensource.org/licenses/MIT

Create configuration file for quotepuller service
=================================================
Gets arguments as command line options and writes
values to re-usable config file.
"""

import argparse
import ConfigParser
import os.path
import sys

import constants

def get_args():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--logpath', required=True)
    _parser.add_argument('--logfmt', required=True)
    _parser.add_argument('--dbconn', required=True)
    _parser.add_argument('--service', required=True)
    return _parser.parse_args()

def set_config(args, fname):
    _config = ConfigParser.SafeConfigParser()
    _sec = constants.CFGSEC_MAIN
    _config.add_section(_sec)
    print('setting logpath to "{}"'.format(args.logpath))
    _config.set(_sec, 'logpath', args.logpath)
    print('setting logfmt to "{}"'.format(args.logfmt))
    _config.set(_sec, 'logfmt', args.logfmt)
    print('setting dbconn to "{}"'.format(args.dbconn))
    _config.set(_sec, 'dbconn', args.dbconn)
    with open(fname, 'wb') as configfile:
        _config.write(configfile)

def init():
    _args = get_args()
    if _args.service != constants.SERVICE_NAME:
        _msg = 'failed! service name "{}" is not the same as "{}"'.format(_args.service,
                constants.SERVICE_NAME)
        print('\033[91m' + _msg + '\033[0m')
        sys.exit(1)
    _fname = constants.CONFIGFILE
    set_config(_args, _fname)

if __name__ == '__main__':
    init()
