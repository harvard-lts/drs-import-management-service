import logging
import os
from typing import Tuple

from healthcheck import HealthCheck
from requests import get, exceptions, HTTPError

from app.health.infrastructure.connectivity_service import ConnectivityService


class DataverseConnectivityService(ConnectivityService):
    __DATAVERSE_CONN_OK_MESSAGE = "Dataverse connection OK"
    __DATAVERSE_CONN_KO_MESSAGE = "Dataverse connection KO"

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        health_check.add_check(self.check_dataverse_connection)

    def check_dataverse_connection(self) -> Tuple[bool, str]:
        logger = logging.getLogger()
        logger.info("Checking Dataverse connectivity...")
        try:
            dataverse_base_url = os.getenv('DATAVERSE_BASE_URL')
            logger.debug("Dataverse base url: " + dataverse_base_url)
            logger.debug("Executing GET operation...")
            get(url=f"{dataverse_base_url}")
            logger.info(self.__DATAVERSE_CONN_OK_MESSAGE)
            return True, self.__DATAVERSE_CONN_OK_MESSAGE
        except (exceptions.ConnectionError, HTTPError) as e:
            logger.error(str(e))
            logger.info(self.__DATAVERSE_CONN_KO_MESSAGE)
            return False, self.__DATAVERSE_CONN_KO_MESSAGE
