"""
.. Copyright (c) 2015 Marshall Farrier
   license http://opensource.org/licenses/MIT

Connection to MongoDB (:mod:`dbconn`)
===================================================

.. currentmodule:: dbconn

Opens and closes db connection.
"""
from pymongo import MongoClient

def job(dbconn, logger, fn):
    _client = MongoClient(dbconn)
    logger.info("db connection opened")
    _ret = fn(_client)
    _client.close()
    logger.info("db connection closed")
    return _ret
