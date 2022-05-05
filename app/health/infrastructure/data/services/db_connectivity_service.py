from typing import Tuple

from healthcheck import HealthCheck

from app.health.infrastructure.connectivity_service import ConnectivityService


class DbConnectivityService(ConnectivityService):

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        def check_mongo_connection() -> Tuple[bool, str]:
            return True, "MongoDB connection OK"

        health_check.add_check(check_mongo_connection)
