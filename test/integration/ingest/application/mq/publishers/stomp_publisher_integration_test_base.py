import time
from abc import ABC

import stomp
from stomp.utils import Frame

from test.integration.ingest.application.mq.stomp_integration_test_base import StompIntegrationTestBase

test_message_received = False


class StompPublisherIntegrationTestBase(StompIntegrationTestBase, ABC):

    def setUp(self) -> None:
        super().setUp()
        self.connection = self._create_subscribed_mq_connection()

    def tearDown(self) -> None:
        self.connection.disconnect()

    def _create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection()
        connection.subscribe(destination=self._get_queue_name(), id=1)
        connection.set_listener('', TestConnectionListener())
        return connection

    def _await_until_message_received_or_timeout(self) -> None:
        timeout = self._get_message_await_timeout()
        while not test_message_received and time.time() < timeout:
            time.sleep(1)

    def _assert_test_message_has_been_received(self) -> None:
        if not test_message_received:
            self.fail(msg="The queue did not receive the published message")


class TestConnectionListener(stomp.ConnectionListener):
    def on_message(self, frame: Frame) -> None:
        global test_message_received
        test_message_received = True
