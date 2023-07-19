from healthcheck import HealthCheck

from app.health.infrastructure.connectivity_service import ConnectivityService
from app.health.infrastructure.data.services.mongo_connectivity_service import MongoConnectivityService


class CompoundConnectivityService(ConnectivityService):
    __connectivity_checkers = [
        MongoConnectivityService(),
    ]

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        for connectivity_checker in self.__connectivity_checkers:
            connectivity_checker.create_connectivity_check(health_check)
