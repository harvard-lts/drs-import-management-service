import json
import logging
from io import BytesIO
from json.decoder import JSONDecodeError
from typing import Any, Callable

from flask import Flask, Response, Request

from app.common.application.middlewares.services.jwt_service import JwtService
from app.common.application.response_status import ResponseStatus


class AuthorizationMiddleware:
    REQUEST_BODY_ENCODING = "utf-8"

    RESPONSE_MESSAGE_MISSING_HEADER = "Missing authorization header in request"
    RESPONSE_MESSAGE_INVALID_TOKEN = "Invalid authorization token"
    RESPONSE_MESSAGE_INVALID_REQUEST_BODY_JSON = "Request body is not a valid JSON"

    def __init__(self, app: Flask) -> None:
        self.__app = app

    def __call__(self, environ: dict, start_response: Callable) -> Any:
        logger = logging.getLogger()
        logger.info("Request entered in authorization middleware")

        request = Request(environ)

        if request.path == "/health":
            logger.info("Authorization skipped for endpoint " + request.path)
            return self.__app(environ, start_response)

        logger.info("Obtaining request body...")
        request_body_str = self.__get_request_body_from_environ(environ)
        logger.info("Request body: " + request_body_str)

        try:
            request_body = json.loads(request_body_str)
        except JSONDecodeError:
            return self.__create_error_response(
                self.RESPONSE_MESSAGE_INVALID_REQUEST_BODY_JSON,
                400,
                environ,
                start_response
            )

        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return self.__create_error_response(
                self.RESPONSE_MESSAGE_MISSING_HEADER,
                401,
                environ,
                start_response
            )
        logger.info("Authorization header: " + authorization_header)

        # Obtaining JWT token by removing "Bearer " prefix from the header value
        jwt_token = authorization_header[7:]

        logger.info("Validating JWT token...")
        jwt_service = JwtService()
        if not jwt_service.validate_jwt_token(
                jwt_token=jwt_token,
                request_body=request_body,
                request_body_encoding=self.REQUEST_BODY_ENCODING
        ):
            return self.__create_error_response(
                self.RESPONSE_MESSAGE_INVALID_TOKEN,
                401,
                environ,
                start_response
            )

        # Updating the environ dictionary request data to include the changes done by JwtService
        self.__update_environ_request_body(environ, request_body)

        return self.__app(environ, start_response)

    def __get_request_body_from_environ(self, environ: dict) -> str:
        length = int(environ.get('CONTENT_LENGTH', '0'))
        body = environ['wsgi.input'].read(length)
        environ['wsgi.input'] = BytesIO(body)
        request_body = body.decode(self.REQUEST_BODY_ENCODING)
        return request_body

    def __update_environ_request_body(self, environ: dict, request_body: dict) -> None:
        request_body_str = json.dumps(request_body).encode(self.REQUEST_BODY_ENCODING)
        environ['wsgi.input'] = BytesIO(request_body_str)
        environ['CONTENT_LENGTH'] = len(request_body_str)

    def __create_error_response(self, message: str, code: int, environ: dict, start_response: Callable) -> Any:
        response = Response(json.dumps(
            {
                "status": ResponseStatus.failure.value,
                "status_code": None,
                "message": message
            }
        ), status=code, mimetype='application/json')
        return response(environ, start_response)
