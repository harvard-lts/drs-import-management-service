import json
import os

from connexion import FlaskApp
from connexion.exceptions import BadRequestProblem

from app.common.application.controllers.responses.error_handlers import render_bad_request_problem
# from app.common.application.middlewares.authorization_middleware import AuthorizationMiddleware
from app.common.application.middlewares.models.jwt_key import JwtKey
from app.drs_import_management_service_resolver import DrsImportManagementServiceResolver
from app.health.application.controllers.health_get_controller import HealthGetController


class DrsImportManagementServiceApp(FlaskApp):

    def __init__(self, import_name: str, **kwargs) -> None:
        super().__init__(import_name, **kwargs)

        self.__setup_controllers()
        # Commenting out to remove the JWT check.  Will replace when it is needed again
        # self.app.wsgi_app = AuthorizationMiddleware(self.app.wsgi_app, self.__get_jwt_keys())

    def __setup_controllers(self) -> None:
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
        self.add_error_handler(BadRequestProblem, render_bad_request_problem)

    def __get_jwt_keys(self) -> dict:
        jwt_keys_dict = json.loads(os.getenv('JWT_KEYS'))
        jwt_keys = {}
        for kid, values in jwt_keys_dict.items():
            jwt_keys[kid] = JwtKey(
                issuer=values['iss'],
                public_key_path=values['public_key_path'],
                depositing_application=values['application_name']
            )
        return jwt_keys

