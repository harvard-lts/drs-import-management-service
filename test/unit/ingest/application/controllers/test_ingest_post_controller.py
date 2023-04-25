from unittest import TestCase
from unittest.mock import Mock

import flask, os

from app.common.application.response_status import ResponseStatus
from app.ingest.application.controllers.ingest_post_controller import IngestPostController
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException
from app.ingest.domain.services.ingest_service import IngestService


class TestIngestPostController(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.REQUEST_ENDPOINT = "/ingest"
        cls.CORRECT_REQUEST_JSON = {
            "package_id": "test",
            "s3_path": "test",
            "s3_bucket_name": "test",
            "depositing_application": "Dataverse",
            "admin_metadata":
                {
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
        os.environ["NO_NOTIFICATIONS"] = "True"

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        ingest_service_mock = Mock(spec=IngestService)
        sut = IngestPostController(ingest_service=ingest_service_mock)

        with self.app.test_request_context(self.REQUEST_ENDPOINT, json=self.CORRECT_REQUEST_JSON):
            actual_response_body, actual_response_http_code = sut.__call__()

        ingest_service_mock.transfer_ingest.assert_called_once()

        expected_response_http_code = 202
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {
            "package_id": "test",
            "status": ResponseStatus.pending.value,
            "status_code": None,
            "message": "Pending transfer to Dropbox"
        }
        self.assertEqual(actual_response_body, expected_response_body)

    def test_call_service_raises_transfer_ingest_exception(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        sut = IngestPostController(ingest_service=ingest_service_stub)

        test_exception = TransferIngestException("test", "test")
        ingest_service_stub.transfer_ingest.side_effect = test_exception

        with self.app.test_request_context(self.REQUEST_ENDPOINT, json=self.CORRECT_REQUEST_JSON):
            actual_response_body, actual_response_http_code = sut.__call__()

        ingest_service_stub.transfer_ingest.assert_called_once()

        expected_response_http_code = 500
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {
            "status": ResponseStatus.failure.value,
            "status_code": "TRANSFER_INGEST_ERROR",
            "message": test_exception.message
        }
        self.assertEqual(actual_response_body, expected_response_body)
