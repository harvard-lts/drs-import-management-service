import os

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from app.ingest.application.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from test.integration.ingest.application.mq.publishers.stomp_publisher_integration_test_base import \
    StompPublisherIntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestTransferReadyQueuePublisher(StompPublisherIntegrationTestBase):

    def test_publish_message_happy_path(self) -> None:
        sut = TransferReadyQueuePublisher()
        test_ingest = create_ingest()
        sut.publish_message(test_ingest)

        self._await_until_message_received_or_timeout()

        self._assert_test_message_has_been_received()

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_TRANSFER_HOST'),
            mq_port=os.getenv('MQ_TRANSFER_PORT'),
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_READY')
