import os

from app.ingest.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.ingest.infrastructure.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from test.integration.ingest.infrastructure.mq.publishers.stomp_publisher_integration_test_base import \
    StompPublisherIntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestProcessReadyQueuePublisher(StompPublisherIntegrationTestBase):

    def test_publish_message_happy_path(self) -> None:
        sut = ProcessReadyQueuePublisher()
        test_ingest = create_ingest()
        sut.publish_message(test_ingest)

        self._await_until_message_received_or_timeout()

        self._assert_test_message_has_been_received()

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_PROCESS_READY')
