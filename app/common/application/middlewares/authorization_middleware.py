import hashlib
import json
import logging
import os
from io import BytesIO
from json.decoder import JSONDecodeError
from typing import Any, Callable

import jwt
from flask import Flask, Response, Request
from jwt import InvalidTokenError


class AuthorizationMiddleware:
    JWT_ENCODING_ALGORITHM = "RS256"
    REQUEST_BODY_ENCODING = "utf-8"

    RESPONSE_MESSAGE_MISSING_HEADER = "Missing authorization header in request"
    RESPONSE_MESSAGE_INVALID_TOKEN = "Invalid authorization token"

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
                self.RESPONSE_MESSAGE_MISSING_HEADER,
                environ,
                start_response
            )

        jwt_token = authorization_header[7:]

        self.__logger.debug("Obtaining JWT token headers...")
        try:
            jwt_token_headers = jwt.get_unverified_header(jwt_token)
        except InvalidTokenError:
            return self.__return_unauthorized_response(
                self.RESPONSE_MESSAGE_INVALID_TOKEN,
                environ,
                start_response
            )

        self.__logger.debug("Validating JWT token headers...")
        if not self.__validate_jwt_headers(jwt_token_headers):
            return self.__return_unauthorized_response(
                self.RESPONSE_MESSAGE_INVALID_TOKEN,
                environ,
                start_response
            )

        self.__logger.debug("Obtaining JWT token body...")
        try:
            jwt_token_body = self.__decode_jwt_token(jwt_token)
        except InvalidTokenError:
            return self.__return_unauthorized_response(
                self.RESPONSE_MESSAGE_INVALID_TOKEN,
                environ,
                start_response
            )

        self.__logger.debug("Obtaining request body...")
        try:
            request_body = json.loads(self.__get_request_body_from_environ(environ))
        except JSONDecodeError:
            response = Response("Malformed JSON body", status=400)
            return response(environ, start_response)

        self.__logger.debug("Validating JWT token body...")
        if not self.__validate_jwt_body(jwt_token_body, request_body):
            return self.__return_unauthorized_response(
                self.RESPONSE_MESSAGE_INVALID_TOKEN,
                environ,
                start_response
            )

        return self.__app(environ, start_response)

    def __return_unauthorized_response(self, message: str, environ: dict, start_response: Callable) -> Any:
        response = Response(message, status=401)
        return response(environ, start_response)

    def __validate_jwt_headers(self, jwt_token_headers: dict) -> bool:
        alg_header = jwt_token_headers.get('alg')
        if alg_header is None:
            return False

        if alg_header != self.JWT_ENCODING_ALGORITHM:
            return False

        typ_header = jwt_token_headers.get('typ')
        if typ_header is None:
            return False

        if typ_header != "JWT":
            return False

        iss_header = jwt_token_headers.get('iss')
        if iss_header is None:
            return False

        if iss_header != os.getenv('JWT_ISSUER_DATAVERSE'):
            return False

        kid_header = jwt_token_headers.get('kid')
        if kid_header is None:
            return False

        if kid_header != os.getenv('JWT_KID_DATAVERSE'):
            return False

        return True

    def __decode_jwt_token(self, jwt_token: str) -> dict:
        jwt_public_key = os.getenv('JWT_PUBLIC_KEY')
        return jwt.decode(
            jwt=jwt_token,
            key=jwt_public_key,
            algorithms=[self.JWT_ENCODING_ALGORITHM]
        )

    def __validate_jwt_body(self, jwt_token_body: dict, request_body: dict) -> bool:
        jwt_body_hash = jwt_token_body.get('body')
        if jwt_body_hash is None:
            return False

        request_body = json.dumps(request_body, separators=(',', ':'))
        request_body_hash = hashlib.md5(request_body.encode()).hexdigest()
        if jwt_body_hash != request_body_hash:
            return False

        return True

    def __get_request_body_from_environ(self, environ: dict) -> str:
        length = int(environ.get('CONTENT_LENGTH', '0'))
        body = environ['wsgi.input'].read(length)
        environ['wsgi.input'] = BytesIO(body)
        request_body = body.decode(self.REQUEST_BODY_ENCODING)
        return request_body
