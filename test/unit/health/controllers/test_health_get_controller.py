from unittest import TestCase

import flask

from health.application.controllers.health_get_controller import HealthGetController


class TestHealthGetController(TestCase):

    def setUp(self) -> None:
        self.app = flask.Flask(__name__)

    def test_call_happy_path(self) -> None:
        sut = HealthGetController()

        with self.app.test_request_context("/health"):
            actual_response_body, actual_response_http_code = sut.__call__()

        expected_response_http_code = 200
        self.assertEqual(actual_response_http_code, expected_response_http_code)

        expected_response_body = "OK!"
        self.assertEqual(actual_response_body, expected_response_body)
