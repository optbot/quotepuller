"""
.. Copyright (c) 2015 Marshall Farrier, Robert Rodrigues, Mark Scappini
   license http://opensource.org/licenses/MIT

Quote puller service main
=========================
"""
import argparse
import logging
import signal
import sys

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

logger = logging.getLogger('quotepuller')

def updatedb(client, rows):
    _dbname = 'optionsMkt'
    _collname = 'equities'
    _db = client[_dbname] 
    _coll = _db[_collname]
    _bulk = _coll.initialize_unordered_bulk_op()
    _n_toinsert = 0
    logger.info('updating active equities')
    for _row in rows:
        _symbol = _row['symbol']
        if _coll.find_one({'symbol': {'$in': [_symbol.lower(), _symbol.upper()]}}) is not None:
            logger.info("equity {} already present".format(_symbol))
        else:
            _bulk.insert(_row)
            _n_toinsert += 1
            logger.debug("equity {} queued for insert into {}.{}".format(_row['symbol'], _dbname, _collname))
    if _n_toinsert > 0:
        try:
            _result = _bulk.execute()
        except BulkWriteError:
            logger.exception("error writing to database")
            raise
        else:
            logger.info("{} records inserted into {}.{}".format(_result['nInserted'], _dbname, _collname))
    else:
        logger.info("no new equities to insert")

def eqpuller(dbconn):
    _rows = rows()
    _client = MongoClient(dbconn)
    logger.info('db connection opened')
    updatedb(_client, _rows)
    _client.close()
    logger.info('db connection closed')

def stop_handler(_signal, frame):
    # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/1112350#1112350
    msg = ('SIGINT' if _signal == signal.SIGINT else 'SIGTERM')
    logger.info('signal {} received. stopping'.format(msg))
    sys.exit(0)

def run():
    logger.info('starting')
    signal.pause()

def init():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--logpath', required=True)
    _parser.add_argument('--logfmt', required=True)
    _parser.add_argument('--dbconn', required=True)
    _args = _parser.parse_args()
    _handler = logging.FileHandler(_args.logpath)
    _formatter = logging.Formatter(_args.logfmt)
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)

def init_tst():
    # hardcoded configuration
    _handler = logging.FileHandler('/mnt/disk1/var/log/optbot/quotepuller/service.log')
    _formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s.%(funcName)s : %(message)s")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)

if __name__ == '__main__':
    init_tst()
    run()
