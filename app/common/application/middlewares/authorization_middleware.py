import hashlib
import json
import logging
import os
from io import BytesIO
from typing import Any, Callable

import jwt
from flask import Flask, Response, Request
from jwt import InvalidTokenError


class AuthorizationMiddleware:
    JWT_ENCODING_ALGORITHM = "RS256"
    REQUEST_BODY_ENCODING = "utf-8"

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
            return self.__return_unauthorized_response(
                "Missing authorization header in request",
                environ,
                start_response
            )

        self.__logger.debug("Decoding JWT token...")
        jwt_token = authorization_header[7:]
        try:
            decoded_jwt_token = self.__decode_jwt_token(jwt_token)
        except InvalidTokenError:
            return self.__return_unauthorized_response(
                "Invalid authorization token",
                environ,
                start_response
            )

        self.__logger.debug("Getting request body...")
        request_body = self.__get_request_body(environ)
        self.__logger.debug("Validating authorization token...")
        if not self.__validate_jwt_token(decoded_jwt_token, request_body):
            return self.__return_unauthorized_response(
                "Invalid authorization token",
                environ,
                start_response
            )

        return self.__app(environ, start_response)

    def __return_unauthorized_response(self, message: str, environ: dict, start_response: Callable) -> Any:
        response = Response(message, status=401)
        return response(environ, start_response)

    def __decode_jwt_token(self, jwt_token: str) -> dict:
        jwt_public_key = os.getenv('JWT_PUBLIC_KEY')
        return jwt.decode(
            jwt=jwt_token,
            key=jwt_public_key,
            algorithms=[self.JWT_ENCODING_ALGORITHM]
        )

    def __get_request_body(self, environ: dict) -> str:
        length = int(environ.get('CONTENT_LENGTH', '0'))
        body = environ['wsgi.input'].read(length)
        environ['wsgi.input'] = BytesIO(body)
        request_body = body.decode(self.REQUEST_BODY_ENCODING)
        return request_body

    def __validate_jwt_token(self, decoded_jwt_token: dict, request_body: str) -> bool:
        jwt_body_hash = decoded_jwt_token.get('body')
        if jwt_body_hash is None:
            return False

        request_body = json.dumps(json.loads(request_body), separators=(',', ':'))
        request_body_hash = hashlib.md5(request_body.encode()).hexdigest()
        if jwt_body_hash != request_body_hash:
            return False

        return True
