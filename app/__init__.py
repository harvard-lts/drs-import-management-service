from flask import Flask

from app.common.application.middlewares.auth_middleware import AuthMiddleware
from app.drs_import_management_service_app import DrsImportManagementServiceApp
from config import config


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.wsgi_app = AuthMiddleware(app.wsgi_app)

    return DrsImportManagementServiceApp(__name__).app
