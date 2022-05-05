from healthcheck import HealthCheck

from app.health.application.controllers.services.connectivity_service import ConnectivityService
from app.health.application.controllers.services.dataverse_connectivity_service import DataverseConnectivityService
from app.health.application.controllers.services.db_connectivity_service import DbConnectivityService
from app.health.application.controllers.services.mq_connectivity_service import MqConnectivityService


class CompoundConnectivityService(ConnectivityService):
    __connectivity_checkers = [DbConnectivityService(), MqConnectivityService(), DataverseConnectivityService()]

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        for connectivity_checker in self.__connectivity_checkers:
            connectivity_checker.create_connectivity_check(health_check)
