"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Connection to MongoDB (:mod:`dbwrapper`)
===================================================

.. currentmodule:: dbwrapper

Opens and closes db connection.
"""
from pymongo import MongoClient

def job(conn_name, logger, fn):
    _client = MongoClient(conn_name)
    logger.info("db connection opened")
    try:
        _ret = fn(logger, _client)
    finally:
        _client.close()
        logger.info("db connection closed")
    return _ret
