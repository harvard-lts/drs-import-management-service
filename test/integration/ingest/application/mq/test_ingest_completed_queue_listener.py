import json
import os
import time
from unittest.mock import patch

from app.ingest.application.mq.ingest_completed_queue_listener import IngestCompletedQueueListener
from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from test.integration.ingest.application.mq.stomp_integration_test_base import StompIntegrationTestBase


class TestIngestCompletedQueueListener(StompIntegrationTestBase):
    def setUp(self) -> None:
        super().setUp()
        self.sut = IngestCompletedQueueListener()

    def tearDown(self) -> None:
        self.sut.disconnect()

    @patch("app.ingest.application.mq.ingest_completed_queue_listener.IngestCompletedQueueListener.on_message")
    def test_on_message_happy_path(self, on_message_mock) -> None:
        self.__send_test_message()

        self.__await_until_on_message_has_calls_or_timeout(on_message_mock)

        if on_message_mock.call_count == 0:
            self.fail(msg="The listener did not receive the published message")

    def __send_test_message(self) -> None:
        connection = self._create_mq_connection(
            MqConnectionParams(
                mq_host=os.getenv('MQ_PROCESS_HOST'),
                mq_port=os.getenv('MQ_PROCESS_PORT'),
                mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
                mq_user=os.getenv('MQ_PROCESS_USER'),
                mq_password=os.getenv('MQ_PROCESS_PASSWORD')
            )
        )

        test_message_json = {}
        test_message_json_str = json.dumps(test_message_json)

        mq_queue_name = os.getenv('MQ_PROCESS_QUEUE')
        connection.send(mq_queue_name, test_message_json_str)

        connection.disconnect()

    def __await_until_on_message_has_calls_or_timeout(self, on_message_mock) -> None:
        timeout = self._get_message_await_timeout()
        while not on_message_mock.call_count and time.time() < timeout:
            time.sleep(1)
