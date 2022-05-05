from healthcheck import HealthCheck

from app.health.infrastructure.connectivity_service import ConnectivityService
from app.health.infrastructure.data.services.db_connectivity_service import DbConnectivityService
from app.health.infrastructure.dataverse.services.dataverse_connectivity_service import DataverseConnectivityService
from app.health.infrastructure.mq.services.mq_connectivity_service import MqConnectivityService


class CompoundConnectivityService(ConnectivityService):
    __connectivity_checkers = [DbConnectivityService(), MqConnectivityService(), DataverseConnectivityService()]

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        for connectivity_checker in self.__connectivity_checkers:
            connectivity_checker.create_connectivity_check(health_check)
