import logging
from typing import Any, Callable

from flask import Flask, Response, Request


class AuthorizationMiddleware:

    def __init__(self, app: Flask) -> None:
        self.__app = app
        self.__logger = logging.getLogger()

    def __call__(self, environ: dict, start_response: Callable) -> Any:
        self.__logger.debug("Request entered in authorization middleware")

        request = Request(environ)

        if request.path == "/health":
            self.__logger.debug("Authorization skipped for endpoint " + request.path)
            return self.__app(environ, start_response)

        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            response = Response("Missing Authorization header in request", status=401)
            return response(environ, start_response)

        return self.__app(environ, start_response)
