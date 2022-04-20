import hashlib
import logging
import os

import jcs
import jwt
from jwt import InvalidTokenError


class JwtService:
    JWT_ENCODING_ALGORITHM = "RS256"

    def validate_jwt_token(self, jwt_token: str, request_body: dict, request_body_encoding: str) -> bool:
        logger = logging.getLogger()
        logger.debug("Obtaining JWT token headers...")
        try:
            jwt_token_headers = jwt.get_unverified_header(jwt_token)
        except InvalidTokenError as ite:
            logger.debug("JWT token is invalid: " + str(ite))
            return False

        logger.debug("Validating JWT token headers...")
        if not self.__validate_jwt_headers(jwt_token_headers):
            logger.debug("Invalid JWT token headers")
            return False

        logger.debug("Obtaining JWT token body...")
        try:
            jwt_token_body = self.__decode_jwt_token(jwt_token)
        except InvalidTokenError as ite:
            logger.debug("JWT token is invalid: " + str(ite))
            return False

        logger.debug("Validating JWT token body...")
        if not self.__validate_jwt_token_body(jwt_token_body, request_body, request_body_encoding):
            logger.debug("Invalid JWT token body")
            return False

        return True

    def __validate_jwt_headers(self, jwt_token_headers: dict) -> bool:
        alg_header = jwt_token_headers.get('alg')
        if alg_header is None or alg_header != self.JWT_ENCODING_ALGORITHM:
            return False

        typ_header = jwt_token_headers.get('typ')
        if typ_header is None or typ_header != "JWT":
            return False

        kid_header = jwt_token_headers.get('kid')
        if kid_header is None or kid_header != os.getenv('DATAVERSE_JWT_KID'):
            return False

        return True

    def __decode_jwt_token(self, jwt_token: str) -> dict:
        jwt_public_key = os.getenv('DATAVERSE_JWT_PUBLIC_KEY')
        return jwt.decode(
            jwt=jwt_token,
            key=jwt_public_key,
            algorithms=[self.JWT_ENCODING_ALGORITHM]
        )

    def __validate_jwt_token_body(self, jwt_token_body: dict, request_body: dict, request_body_encoding: str) -> bool:
        issuer = jwt_token_body.get('iss')
        if issuer is None or issuer != os.getenv('DATAVERSE_JWT_ISSUER'):
            return False

        jwt_body_hash = jwt_token_body.get('bodySHA256Hash')
        if jwt_body_hash is None:
            return False

        request_body = jcs.canonicalize(request_body).decode(request_body_encoding)
        request_body_hash = hashlib.sha256(request_body.encode()).hexdigest()

        if jwt_body_hash != request_body_hash:
            return False

        return True
