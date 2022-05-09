import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from requests import Response

from app.drs_import_management_service_app import DrsImportManagementServiceApp
from config import config

LOG_FILE_DEFAULT_PATH = "/home/dimsuser/logs/dims.log"
LOG_FILE_DEFAULT_LEVEL = logging.DEBUG
LOG_FILE_MAX_SIZE_BYTES = 2 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 1


def create_app(config_name: str = 'default') -> Flask:
    if config_name != 'testing':
        configure_logger()

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app = DrsImportManagementServiceApp(__name__).app
    disable_cached_responses(app)

    return app


def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response


def configure_logger() -> None:
    log_file_path = os.getenv('LOG_FILE_PATH', LOG_FILE_DEFAULT_PATH)
    logger = logging.getLogger()

    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=LOG_FILE_MAX_SIZE_BYTES,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    logger.addHandler(file_handler)

    log_level = os.getenv('LOG_LEVEL', LOG_FILE_DEFAULT_LEVEL)
    logger.setLevel(log_level)
