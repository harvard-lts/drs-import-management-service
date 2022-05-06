from typing import Tuple

from healthcheck import HealthCheck
from pymongo.errors import PyMongoError

from app.common.infrastructure.data.mongo_interactor import MongoInteractor
from app.health.infrastructure.connectivity_service import ConnectivityService


class MongoConnectivityService(ConnectivityService, MongoInteractor):
    __MONGO_CONN_OK_MESSAGE = "MongoDB connection OK"
    __MONGO_CONN_KO_MESSAGE = "MongoDB connection KO"

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        self._logger.info("Checking MongoDB connectivity...")

        def check_mongo_connection() -> Tuple[bool, str]:
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

        health_check.add_check(check_mongo_connection)
