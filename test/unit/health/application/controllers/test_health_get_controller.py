from unittest import TestCase
from unittest.mock import Mock

import flask

from app.health.application.controllers.health_get_controller import HealthGetController
from app.health.application.controllers.services.exceptions.get_current_commit_hash_exception import \
    GetCurrentCommitHashException
from app.health.application.controllers.services.git_service import GitService


class TestHealthGetController(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.REQUEST_ENDPOINT = "/health"

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        git_service_stub = Mock(spec=GitService)
        git_service_stub.get_current_commit_hash.return_value = "test"
        sut = HealthGetController(git_service=git_service_stub)

        with self.app.test_request_context(self.REQUEST_ENDPOINT):
            actual_response_body, actual_response_http_code = sut.__call__()

        git_service_stub.get_current_commit_hash.assert_called_once()

        expected_response_http_code = 200
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = "OK! test"
        self.assertEqual(actual_response_body, expected_response_body)

    def test_call_git_service_raises_get_current_commit_hash_exception(self) -> None:
        git_service_stub = Mock(spec=GitService)
        git_service_stub.get_current_commit_hash.side_effect = GetCurrentCommitHashException("test")
        sut = HealthGetController(git_service=git_service_stub)

        with self.app.test_request_context(self.REQUEST_ENDPOINT):
            actual_response_body, actual_response_http_code = sut.__call__()

        git_service_stub.get_current_commit_hash.assert_called_once()

        expected_response_http_code = 500
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        # TODO: Actual response
        expected_response_body = "NO OK! There was an error when getting current git commit hash. Reason was: test"
        self.assertEqual(actual_response_body, expected_response_body)
