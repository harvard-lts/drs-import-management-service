from unittest import TestCase
from unittest.mock import Mock

import flask

from app.ingest.application.controllers.ingest_post_controller import IngestPostController
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException
from app.ingest.domain.services.ingest_service import IngestService


class TestIngestPostController(TestCase):
    __REQUEST_ENDPOINT = "/ingest"

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        ingest_service_mock = Mock(spect=IngestService)
        sut = IngestPostController(ingest_service_mock)

        with self.app.test_request_context(self.__REQUEST_ENDPOINT):
            actual_response_body, actual_response_http_code = sut.__call__()

        ingest_service_mock.transfer_ingest.assert_called_once()

        expected_response_http_code = 202
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {"data": {"ingest_status": "processing_ingest"}, "error": None}
        self.assertEqual(actual_response_body, expected_response_body)

    def test_call_service_raises_transfer_ingest_exception(self) -> None:
        ingest_service_stub = Mock(spect=IngestService)
        sut = IngestPostController(ingest_service_stub)

        test_exception = TransferIngestException("test", "test")
        ingest_service_stub.transfer_ingest.side_effect = test_exception

        with self.app.test_request_context(self.__REQUEST_ENDPOINT):
            actual_response_body, actual_response_http_code = sut.__call__()

        ingest_service_stub.transfer_ingest.assert_called_once()

        expected_response_http_code = 500
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {"data": None, "error": test_exception.message}
        self.assertEqual(actual_response_body, expected_response_body)
