from flask import Flask

from config import config
from app.import_management_service_app import ImportManagementServiceApp


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return ImportManagementServiceApp(__name__).app
