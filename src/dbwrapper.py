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
    _client = MongoClient()
    logger.info("db connection opened")
    _ret = fn(logger, _client)
    _client.close()
    logger.info("db connection closed")
    return _ret
