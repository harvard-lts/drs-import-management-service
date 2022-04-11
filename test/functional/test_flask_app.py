import json
import os
from datetime import datetime, timedelta
from os.path import join, dirname
from unittest import TestCase

import jwt
from dotenv import load_dotenv
from flask import Response
from flask.testing import FlaskClient

from app import create_app


class TestFlaskApp(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST_REQUEST_BODY = {
            "package_id": "test_package_id",
            "s3_path": "test",
            "s3_bucket_name": "test",
            "admin_metadata": {
                "accessFlag": "N",
                "contentModel": "opaque",
                "depositingSystem": "Harvard Dataverse",
                "firstGenerationInDrs": "unspecified",
                "objectRole": "CG:DATASET",
                "usageClass": "LOWUSE",
                "storageClass": "AR",
                "ownerCode": "123",
                "billingCode": "456",
                "resourceNamePattern": "pattern",
                "urnAuthorityPath": "path",
                "depositAgent": "789",
                "depositAgentEmail": "someone@mailinator.com",
                "successEmail": "winner@mailinator.com",
                "failureEmail": "loser@mailinator.com",
                "successMethod": "method",
                "adminCategory": "root"
            }
        }
        cls.TEST_INGEST_REQUEST_BODY_CANONICAL_HASH = "698dff27ee8e13447841a3564175e0e7909f96798b8f67b4ba2462f5f107568b"
        cls.INVALID_AUTHORIZATION_TOKEN_RESPONSE_BODY = {
            "message": "Invalid authorization token",
            "status": "failure",
            "status_code": None
        }

    def setUp(self) -> None:
        load_dotenv(join(dirname(__file__), '.test.env'))
        self.test_app = create_app('testing')

    def test_health_endpoint_happy_path(self) -> None:
        with self.test_app.test_client() as test_client:
            response = test_client.get("/health")
            actual_response_status_code = response.status_code
            expected_response_status_code = 200
            assert actual_response_status_code == expected_response_status_code

    def test_ingest_endpoint_happy_path(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header()
            )

            actual_response_status_code = response.status_code
            expected_response_status_code = 202
            assert actual_response_status_code == expected_response_status_code

            actual_response_body = response.get_json()
            expected_response_body = {
                "message": "Added to Queue",
                "package_id": "test_package_id",
                "status": "pending",
                "status_code": None
            }
            assert actual_response_body == expected_response_body

    def test_ingest_endpoint_invalid_request_body(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header(),
                request_body="{invalid request body}"
            )

            actual_response_status_code = response.status_code
            expected_response_status_code = 400
            assert actual_response_status_code == expected_response_status_code

            actual_response_body = response.get_json()
            expected_response_body = {
                "message": "Request body is not a valid JSON",
                "status": "failure",
                "status_code": None
            }
            assert actual_response_body == expected_response_body

    def test_ingest_endpoint_missing_authorization_header(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client
            )

            actual_response_status_code = response.status_code
            expected_response_status_code = 401
            assert actual_response_status_code == expected_response_status_code

            actual_response_body = response.get_json()
            expected_response_body = {
                "message": "Missing authorization header in request",
                "status": "failure",
                "status_code": None
            }
            assert actual_response_body == expected_response_body

    def test_ingest_endpoint_expired_authorization_token(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header(
                    expiration_date_time=datetime.utcnow() - timedelta(hours=1)
                )
            )
            self.__assert_invalid_authorization_token_response(response)

    def test_ingest_endpoint_invalid_jwt_issuer(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header(
                    issuer="Invalid Issuer"
                )
            )
            self.__assert_invalid_authorization_token_response(response)

    def test_ingest_endpoint_invalid_jwt_kid(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header(
                    kid="Invalid Kid"
                )
            )
            self.__assert_invalid_authorization_token_response(response)

    def test_ingest_endpoint_jwt_not_corresponding_to_the_request_body(self) -> None:
        with self.test_app.test_client() as test_client:
            response = self.__post_ingest_endpoint(
                test_client=test_client,
                authorization_header=self.__create_ingest_authorization_header(),
                request_body=json.dumps({"test": "test"})
            )
            self.__assert_invalid_authorization_token_response(response)

    def __post_ingest_endpoint(
            self,
            test_client: FlaskClient,
            authorization_header: str = None,
            request_body: str = None
    ) -> Response:
        headers = {
            "Content-Type": "application/json"
        }
        if authorization_header is not None:
            headers["Authorization"] = authorization_header

        if request_body is None:
            request_body = json.dumps(self.TEST_INGEST_REQUEST_BODY)

        response = test_client.post(
            "/ingest",
            headers=headers,
            data=request_body
        )
        return response

    def __create_ingest_authorization_header(
            self,
            issuer: str = None,
            kid: str = None,
            expiration_date_time: datetime = datetime.utcnow() + timedelta(seconds=30)
    ) -> str:
        if issuer is None:
            issuer = os.getenv('JWT_ISSUER_DATAVERSE')

        if kid is None:
            kid = os.getenv('JWT_KID_DATAVERSE')

        return "Bearer " + jwt.encode(
            key=os.getenv('JWT_PRIVATE_KEY'),
            payload={
                "iss": issuer,
                "bodySHA256Hash": self.TEST_INGEST_REQUEST_BODY_CANONICAL_HASH,
                "iat": datetime.timestamp(datetime.utcnow()),
                "exp": datetime.timestamp(expiration_date_time)
            },
            algorithm="RS256",
            headers={
                "alg": "RS256",
                "typ": "JWT",
                "kid": kid
            }
        )

    def __assert_invalid_authorization_token_response(self, response: Response) -> None:
        actual_response_status_code = response.status_code
        expected_response_status_code = 401
        assert actual_response_status_code == expected_response_status_code

        actual_response_body = response.get_json()
        expected_response_body = self.INVALID_AUTHORIZATION_TOKEN_RESPONSE_BODY
        assert actual_response_body == expected_response_body
