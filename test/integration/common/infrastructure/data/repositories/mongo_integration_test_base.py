from abc import ABC, abstractmethod

from pymongo import MongoClient
from pymongo.database import Database

from app.ingest.infrastructure.data.repositories.db_connection_params import DbConnectionParams
from test.integration.integration_test_base import IntegrationTestBase


class MongoIntegrationTestBase(IntegrationTestBase, ABC):

    def setUp(self) -> None:
        super().setUp()
        self.__clean_database()

    def tearDown(self) -> None:
        self.__clean_database()

    def __clean_database(self) -> None:
        db = self._get_database()
        db[self._get_db_collection_name()].delete_many({})

    def _get_database(self) -> Database:
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
        pass

    @abstractmethod
    def _get_db_collection_name(self) -> str:
        pass
