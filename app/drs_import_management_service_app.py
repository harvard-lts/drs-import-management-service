from connexion import FlaskApp

from app.ingest.application.mq.listeners.process_status_queue_listener import ProcessStatusQueueListener
from app.ingest.application.mq.listeners.transfer_status_queue_listener import TransferStatusQueueListener
from app.drs_import_management_service_resolver import DrsImportManagementServiceResolver
from app.health.application.controllers.health_get_controller import HealthGetController


class DrsImportManagementServiceApp(FlaskApp):

    def __init__(self, import_name: str, **kwargs) -> None:
        super().__init__(import_name, **kwargs)

        self.__setup_controllers()
        self.__setup_queue_listeners()

    def __setup_controllers(self):
        health_controller = HealthGetController()
        health_controller.__name__ = "app.health.application.controllers.health_get_controller.HealthGetController"
        self.add_url_rule(
            rule="/health",
            endpoint="health",
            view_func=health_controller,
        )
        self.add_api(
            specification="openapi/dims_0.1.0.yaml",
            resolver=DrsImportManagementServiceResolver()
        )

    def __setup_queue_listeners(self) -> None:
        TransferStatusQueueListener()
        ProcessStatusQueueListener()
