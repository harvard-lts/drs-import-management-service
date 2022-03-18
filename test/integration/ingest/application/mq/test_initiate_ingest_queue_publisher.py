import os
import time

import stomp
from stomp.utils import Frame

from app.ingest.application.mq.initiate_ingest_queue_publisher import InitiateIngestQueuePublisher
from test.integration.integration_test_base import IntegrationTestBase

test_message_received = False


class TestInitiateIngestQueuePublisher(IntegrationTestBase):
    __STOMP_CONN_HEARTBEATS_MS = 40000
    __MESSAGE_AWAIT_TIMEOUT_SECONDS = 30

    def setUp(self) -> None:
        super().setUp()
        self.__create_mq_connection()

    def test_publish_message_happy_path(self) -> None:
        sut = InitiateIngestQueuePublisher()
        sut.publish_message()

        self.__await_until_message_received_or_timeout()

        if not test_message_received:
            self.fail(msg="The queue did not receive the published message")

    def __create_mq_connection(self) -> stomp.Connection:
        mq_host = os.getenv('MQ_HOST')
        mq_port = os.getenv('MQ_PORT')
        mq_queue_name = os.getenv('MQ_QUEUE')
        mq_ssl_enabled = os.getenv('MQ_SSL_ENABLED')
        mq_user = os.getenv('MQ_USER')
        mq_password = os.getenv('MQ_PASSWORD')

        connection = stomp.Connection(
            host_and_ports=[(mq_host, mq_port)],
            heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
            keepalive=True
        )

        if os.getenv(mq_ssl_enabled) == 'True':
            connection.set_ssl([(mq_host, mq_port)])

        connection.connect(
            mq_user,
            mq_password,
            wait=True
        )

        connection.subscribe(destination=mq_queue_name, id=1)
        connection.set_listener('', TestConnectionListener())

        return connection

    def __await_until_message_received_or_timeout(self) -> None:
        timeout = time.time() + self.__MESSAGE_AWAIT_TIMEOUT_SECONDS
        while not test_message_received and time.time() < timeout:
            time.sleep(1)


class TestConnectionListener(stomp.ConnectionListener):
    def on_message(self, frame: Frame) -> None:
        global test_message_received
        test_message_received = True
