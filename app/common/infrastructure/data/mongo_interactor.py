"""
This module defines a MongoInteractor, which is an abstract class intended
to define common behavior for MongoDB-implemented components.
"""
import logging
import os
from abc import ABC

from pymongo import MongoClient
from pymongo.database import Database

from app.common.infrastructure.data.repositories.db_connection_params import DbConnectionParams


class MongoInteractor(ABC):
    _MONGO_OPERATION_MAX_RETRIES = 2
    __MONGO_CONN_TIMEOUT_MS = 5000

    def __init__(self) -> None:
        self._logger = logging.getLogger()

    def _get_database(self) -> Database:
        """
        Retrieves a Database object by connecting to MongoDB via MongoClient
        """
        db_connection_params = self.__get_db_connection_params()
        self._logger.debug("Obtaining MongoDB client...")
        db_name = db_connection_params.db_name
        client = MongoClient(
            host=db_connection_params.db_hosts,
            port=db_connection_params.db_port,
            username=db_connection_params.db_user,
            password=db_connection_params.db_password,
            authSource=db_name,
            serverSelectionTimeoutMS=self.__MONGO_CONN_TIMEOUT_MS
        )
        return client[db_name]

    def __get_db_connection_params(self) -> DbConnectionParams:
        """
        Retrieves the DB connection params necessary for creating the connection
        """
        return DbConnectionParams(
            db_hosts=[os.getenv('MONGODB_HOST_1'), os.getenv('MONGODB_HOST_2'), os.getenv('MONGODB_HOST_3')],
            db_port=int(os.getenv('MONGODB_PORT')),
            db_name=os.getenv('MONGODB_DB_NAME'),
            db_user=os.getenv('MONGODB_USER'),
            db_password=os.getenv('MONGODB_PASSWORD'),
        )
