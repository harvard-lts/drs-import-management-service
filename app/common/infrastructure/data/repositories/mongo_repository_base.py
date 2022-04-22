"""
This module defines a MongoRepositoryBase, which is an abstract class intended
to define common behavior for MongoDB-implemented repositories.
"""

from abc import ABC, abstractmethod

from pymongo import MongoClient
from pymongo.database import Database

from app.ingest.infrastructure.data.repositories.db_connection_params import DbConnectionParams


class MongoRepositoryBase(ABC):

    def _get_database(self) -> Database:
        """
        Retrieves a Database object by connecting to MongoDB via MongoClient
        """
        db_connection_params = self._get_db_connection_params()
        db_name = db_connection_params.db_name
        client = MongoClient(
            host=db_connection_params.db_host,
            port=db_connection_params.db_port,
            username=db_connection_params.db_user,
            password=db_connection_params.db_password,
            authSource=db_name
        )
        db = client[db_name]
        return db

    @abstractmethod
    def _get_db_connection_params(self) -> DbConnectionParams:
        """
        Retrieves the DB connection params necessary for creating the connection
        """
