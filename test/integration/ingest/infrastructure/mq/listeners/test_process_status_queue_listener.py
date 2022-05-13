import os
from unittest.mock import patch

from app.ingest.infrastructure.mq.listeners.process_status_queue_listener import ProcessStatusQueueListener
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from test.integration.common.infrastructure.mq.listeners.stomp_listener_integration_test_base import \
    StompListenerIntegrationTestBase


class TestProcessStatusQueueListener(StompListenerIntegrationTestBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_MESSAGE = {
            "package_id": "test",
            "application_name": "Dataverse",
            "batch_ingest_status": "successful",
            "drs_url": "test",
            "message": "test"
        }

    def setUp(self) -> None:
        super().setUp()
        self.sut = ProcessStatusQueueListener()

    def tearDown(self) -> None:
        self.sut.disconnect()

    @patch("app.ingest.infrastructure.mq.listeners.process_status_queue_listener.ProcessStatusQueueListener"
           "._handle_received_message")
    def test_on_message_happy_path(self, on_message_mock) -> None:
        self._send_test_message(self.TEST_MESSAGE)
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

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_PROCESS_STATUS')
