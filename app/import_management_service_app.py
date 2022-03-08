from connexion import FlaskApp

from .health.application.controllers.health_get_controller import HealthGetController


class ImportManagementServiceApp(FlaskApp):

    def __init__(self, import_name: str, **kwargs) -> None:
        super().__init__(import_name, **kwargs)

        health_controller = HealthGetController()
        health_controller.__name__ = "health.application.controllers.health_get_controller.HealthGetController"
        self.add_url_rule(
            rule="/health",
            endpoint="health",
            view_func=health_controller,
        )
