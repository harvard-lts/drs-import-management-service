import json
import time
from abc import ABC, abstractmethod

import stomp
from stomp.utils import Frame

from test.integration.common.infrastructure.mq.stomp_integration_test_base import StompIntegrationTestBase


class StompPublisherIntegrationTestBase(StompIntegrationTestBase, ABC):

    def setUp(self) -> None:
        super().setUp()
        self.received_frame = None
        self.connection = self._create_subscribed_mq_connection()

    def tearDown(self) -> None:
        self.connection.disconnect()

    def _create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection()
        connection.subscribe(destination=self._get_queue_name(), id=self._get_queue_name() + "-test-connection")
        connection.set_listener(self._get_queue_name() + "-test-listener",
                                StompPublisherIntegrationTestBase.TestConnectionListener(self))
        return connection

    def _await_until_message_received_or_timeout(self) -> None:
        timeout = self._get_message_await_timeout()
        while self.received_frame is None and time.time() < timeout:
            time.sleep(1)

    def _assert_test_message_has_been_received(self) -> None:
        if self.received_frame is None:
            self.fail(msg="The queue did not receive the published message")

        actual_headers = self.received_frame.headers

        actual_original_queue_header = actual_headers['original_queue']
        expected_original_queue_header = self._get_queue_name()
        self.assertEqual(actual_original_queue_header, expected_original_queue_header)

        actual_retry_count_header = actual_headers['retry_count']
        expected_retry_count_header = "0"
        self.assertEqual(actual_retry_count_header, expected_retry_count_header)

        actual_body_str = self.received_frame.body
        expected_body_str = json.dumps(self._get_expected_body())
        self.assertEqual(actual_body_str, expected_body_str)

    @abstractmethod
    def _get_expected_body(self) -> dict:
        pass

    class TestConnectionListener(stomp.ConnectionListener):
        def __init__(self, outer_test) -> None:
            self.outer_test = outer_test

        def on_message(self, frame: Frame) -> None:
            self.outer_test.received_frame = frame
