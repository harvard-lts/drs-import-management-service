from unittest import TestCase
from unittest.mock import Mock, patch

import flask

from app.common.application.response_status import ResponseStatus
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

    @patch(
        "app.health.application.controllers.health_get_controller.HealthGetController."
        "_HealthGetController__execute_health_check"
    )
    def test_call_happy_path(self, execute_health_check_stub) -> None:
        git_service_stub = Mock(spec=GitService)
        git_service_stub.get_current_commit_hash.return_value = "test"

        sut = HealthGetController(
            git_service=git_service_stub
        )

        test_response_message = "test"
        test_response_code = 200
        test_response_headers = {}
        execute_health_check_stub.return_value = test_response_message, test_response_code, test_response_headers

        with self.app.test_request_context(self.REQUEST_ENDPOINT):
            actual_response_message, actual_response_status, actual_response_headers = sut.__call__()

        git_service_stub.get_current_commit_hash.assert_called_once()

        expected_response_message = test_response_message
        self.assertEqual(actual_response_message, expected_response_message)

        expected_response_status = test_response_code
        self.assertEqual(actual_response_status, expected_response_status)

        expected_response_headers = test_response_headers
        self.assertEqual(actual_response_headers, expected_response_headers)

    def test_call_git_service_raises_get_current_commit_hash_exception(self) -> None:
        git_service_stub = Mock(spec=GitService)
        test_exception = GetCurrentCommitHashException("test")
        git_service_stub.get_current_commit_hash.side_effect = test_exception

        sut = HealthGetController(
            git_service=git_service_stub
        )

        with self.app.test_request_context(self.REQUEST_ENDPOINT):
            actual_response_body, actual_response_http_code = sut.__call__()

        git_service_stub.get_current_commit_hash.assert_called_once()

        expected_response_http_code = 500
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = {
            "status": ResponseStatus.failure.value,
            "status_code": "GET_CURRENT_COMMIT_ERROR",
            "message": test_exception.message
        }
        self.assertEqual(actual_response_body, expected_response_body)
