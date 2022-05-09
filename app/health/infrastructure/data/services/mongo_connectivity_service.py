from typing import Tuple

from healthcheck import HealthCheck
from pymongo.errors import PyMongoError

from app.common.infrastructure.data.mongo_interactor import MongoInteractor
from app.health.infrastructure.connectivity_service import ConnectivityService


class MongoConnectivityService(ConnectivityService, MongoInteractor):
    __MONGO_CONN_OK_MESSAGE = "MongoDB connection OK"
    __MONGO_CONN_KO_MESSAGE = "MongoDB connection KO"

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        health_check.add_check(self.check_mongo_connection)

    def check_mongo_connection(self) -> Tuple[bool, str]:
        self._logger.info("Checking MongoDB connectivity...")
        try:
            mongo_client = self._get_database().client
            mongo_server_info = mongo_client.server_info()
            self._logger.debug(str(mongo_server_info))
            self._logger.info(self.__MONGO_CONN_OK_MESSAGE)
            return True, self.__MONGO_CONN_OK_MESSAGE
        except PyMongoError as pme:
            self._logger.error(str(pme))
            self._logger.info(self.__MONGO_CONN_KO_MESSAGE)
            return False, self.__MONGO_CONN_KO_MESSAGE
