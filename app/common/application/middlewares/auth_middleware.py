from typing import Any, Callable

from flask import Flask, Response


class AuthMiddleware:

    def __init__(self, app: Flask) -> None:
        self.__app = app

    def __call__(self, environ: dict, start_response: Callable) -> Any:
        auth_header = environ.get('Authorization')
        if not auth_header:
            response = Response("Missing Authorization header", status=403)
            return response(environ, start_response)

        return self.__app(environ, start_response)
