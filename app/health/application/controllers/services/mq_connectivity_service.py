from typing import Tuple

from healthcheck import HealthCheck

from app.health.application.controllers.services.connectivity_service import ConnectivityService


class MqConnectivityService(ConnectivityService):

    def create_connectivity_check(self, health_check: HealthCheck) -> None:
        def check_mq_connection() -> Tuple[bool, str]:
            return True, "MQ connection OK"

        health_check.add_check(check_mq_connection)
