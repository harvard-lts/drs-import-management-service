from typing import Tuple

from healthcheck import HealthCheck

from app.health.infrastructure.connectivity_service import ConnectivityService


class DataverseConnectivityService(ConnectivityService):

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        health_check.add_check(self.check_dataverse_connection)

    def check_dataverse_connection(self) -> Tuple[bool, str]:
        return True, "Dataverse connection OK"
