import hashlib
import logging
import os

import jcs
import jwt
from cryptography.hazmat.primitives.asymmetric.types import PUBLIC_KEY_TYPES
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from jwt import InvalidTokenError


class JwtService:
    JWT_ENCODING_ALGORITHM = "RS256"
    JWT_HEADER_TYP_VALUE = "JWT"

    def __init__(self) -> None:
        self.__logger = logging.getLogger()

    def validate_jwt_token(self, jwt_token: str, request_body: dict, request_body_encoding: str) -> bool:
        self.__logger.debug("Obtaining JWT token headers...")
        try:
            jwt_token_headers = jwt.get_unverified_header(jwt_token)
        except InvalidTokenError as ite:
            self.__logger.debug("JWT token is invalid: " + str(ite))
            return False

        self.__logger.debug("Validating JWT token headers...")
        if not self.__validate_jwt_headers(jwt_token_headers):
            self.__logger.debug("Invalid JWT token headers")
            return False

        self.__logger.debug("Obtaining JWT token body...")
        try:
            jwt_token_body = self.__decode_jwt_token(jwt_token)
        except Exception as e:
            self.__logger.debug("Error while obtaining JWT token body: " + str(e))
            return False

        self.__logger.debug("Validating JWT token body...")
        if not self.__validate_jwt_token_body(jwt_token_body, request_body, request_body_encoding):
            self.__logger.debug("Invalid JWT token body")
            return False

        return True

    def __validate_jwt_headers(self, jwt_token_headers: dict) -> bool:
        alg_header = jwt_token_headers.get('alg')
        if alg_header is None or alg_header != self.JWT_ENCODING_ALGORITHM:
            self.__logger.debug(
                "Received 'alg' header: '" + str(alg_header) + "'. Expected: '" + self.JWT_ENCODING_ALGORITHM + "'"
            )
            return False

        typ_header = jwt_token_headers.get('typ')
        if typ_header is None or typ_header != self.JWT_HEADER_TYP_VALUE:
            self.__logger.debug(
                "Received 'typ' header: '" + str(typ_header) + "'. Expected: '" + self.JWT_HEADER_TYP_VALUE + "'"
            )
            return False

        kid_header = jwt_token_headers.get('kid')
        jwt_header_kid_value = os.getenv('DATAVERSE_JWT_KID')
        if kid_header is None or kid_header != jwt_header_kid_value:
            self.__logger.debug(
                "Received 'kid' header: '" + str(kid_header) + "'. Expected: '" + jwt_header_kid_value + "'"
            )
            return False

        return True

    def __decode_jwt_token(self, jwt_token: str) -> dict:
        jwt_public_key = self.__get_jwt_public_key()
        return jwt.decode(
            jwt=jwt_token,
            key=jwt_public_key,
            algorithms=[self.JWT_ENCODING_ALGORITHM]
        )

    def __get_jwt_public_key(self) -> PUBLIC_KEY_TYPES:
        self.__logger.debug("Obtaining JWT public key from file...")
        with open(os.getenv('DATAVERSE_JWT_PUBLIC_KEY_FILE_PATH'), "rb") as key_file:
            key = key_file.read()

        self.__logger.debug("Loading JWT public key...")
        jwt_public_key = load_pem_public_key(key)

        return jwt_public_key

    def __validate_jwt_token_body(self, jwt_token_body: dict, request_body: dict, request_body_encoding: str) -> bool:
        issuer = jwt_token_body.get('iss')
        jwt_body_issuer_value = os.getenv('DATAVERSE_JWT_ISSUER')
        if issuer is None or issuer != jwt_body_issuer_value:
            self.__logger.debug(
                "Received 'iss' body param: " + str(issuer) + ". Expected: " + jwt_body_issuer_value
            )
            return False

        jwt_body_hash = jwt_token_body.get('bodySHA256Hash')
        if jwt_body_hash is None:
            self.__logger.debug("Missing 'bodySHA256Hash' body param")
            return False

        self.__logger.debug("Validating 'bodySHA256Hash' body param...")
        request_body = jcs.canonicalize(request_body).decode(request_body_encoding)
        request_body_hash = hashlib.sha256(request_body.encode()).hexdigest()
        if jwt_body_hash != request_body_hash:
            self.__logger.debug("Body param 'bodySHA256Hash' do not match actual request body hash")
            return False

        return True
