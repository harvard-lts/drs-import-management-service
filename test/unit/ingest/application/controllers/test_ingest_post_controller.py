from unittest import TestCase

import flask

from ingest.application.controllers.ingest_post_controller import IngestPostController


class TestIngestPostController(TestCase):

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        sut = IngestPostController()

        with self.app.test_request_context("/ingest"):
            actual_response_body, actual_response_http_code = sut.__call__()

        expected_response_http_code = 202
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {"data": {"ingest_status": "processing_ingest"}}
        self.assertEqual(actual_response_body, expected_response_body)
