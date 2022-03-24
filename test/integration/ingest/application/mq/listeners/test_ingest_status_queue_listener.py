import os
from unittest.mock import patch

from app.ingest.application.mq.listeners.ingest_status_queue_listener import IngestStatusQueueListener
from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from test.integration.ingest.application.mq.listeners.stomp_listener_integration_test_base import \
    StompListenerIntegrationTestBase


class TestIngestStatusQueueListener(StompListenerIntegrationTestBase):
    def setUp(self) -> None:
        super().setUp()
        self.sut = IngestStatusQueueListener()

    def tearDown(self) -> None:
        self.sut.disconnect()

    @patch("app.ingest.application.mq.listeners.ingest_status_queue_listener.IngestStatusQueueListener.on_message")
    def test_on_message_happy_path(self, on_message_mock) -> None:
        self._send_test_message(mq_queue_name=os.getenv('MQ_PROCESS_QUEUE_DRS_INGEST_STATUS'))
        self._await_until_on_message_has_calls_or_timeout(on_message_mock)
        self._assert_on_message_has_calls(on_message_mock)

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )
