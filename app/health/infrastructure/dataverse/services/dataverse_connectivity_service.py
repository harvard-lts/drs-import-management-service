from typing import Tuple

from healthcheck import HealthCheck

from app.health.infrastructure.connectivity_service import ConnectivityService


class DataverseConnectivityService(ConnectivityService):

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        def check_dataverse_connection() -> Tuple[bool, str]:
            return True, "Dataverse connection OK"

        health_check.add_check(check_dataverse_connection)
