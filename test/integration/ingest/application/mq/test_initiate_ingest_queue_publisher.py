import os
import time

import stomp
from stomp.utils import Frame

from app.ingest.application.mq.initiate_ingest_queue_publisher import InitiateIngestQueuePublisher
from test.integration.ingest.application.mq.stomp_integration_test_base import StompIntegrationTestBase

test_message_received = False


class TestInitiateIngestQueuePublisher(StompIntegrationTestBase):

    def setUp(self) -> None:
        super().setUp()
        self.connection = self.__create_subscribed_mq_connection()

    def tearDown(self) -> None:
        self.connection.disconnect()

    def test_publish_message_happy_path(self) -> None:
        sut = InitiateIngestQueuePublisher()
        sut.publish_message()

        self.__await_until_message_received_or_timeout()

        if not test_message_received:
            self.fail(msg="The queue did not receive the published message")

    def __create_subscribed_mq_connection(self) -> stomp.Connection:
        mq_queue_name = os.getenv('MQ_QUEUE')

        connection = self._create_mq_connection()
        connection.subscribe(destination=mq_queue_name, id=1)

        connection.set_listener('', TestConnectionListener())

        return connection

    def __await_until_message_received_or_timeout(self) -> None:
        timeout = self._get_message_await_timeout()
        while not test_message_received and time.time() < timeout:
            time.sleep(1)


class TestConnectionListener(stomp.ConnectionListener):
    def on_message(self, frame: Frame) -> None:
        global test_message_received
        test_message_received = True
