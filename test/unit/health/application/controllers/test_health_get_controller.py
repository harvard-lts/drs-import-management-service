from unittest import TestCase
from unittest.mock import Mock

import flask

from app.health.application.controllers.health_get_controller import HealthGetController
from app.ingest.application.controllers.services.git_service import GitService


class TestHealthGetController(TestCase):

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        git_service_stub = Mock(spec=GitService)
        git_service_stub.get_commit_hash.return_value = "test"
        sut = HealthGetController(git_service=git_service_stub)

        with self.app.test_request_context("/health"):
            actual_response_body, actual_response_http_code = sut.__call__()

        expected_response_http_code = 200
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = "OK! test"
        self.assertEqual(actual_response_body, expected_response_body)
