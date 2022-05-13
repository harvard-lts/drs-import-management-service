import os

from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.ingest.infrastructure.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from test.integration.common.infrastructure.mq.publishers.stomp_publisher_integration_test_base import \
    StompPublisherIntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestTransferReadyQueuePublisher(StompPublisherIntegrationTestBase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()

    def test_publish_message_happy_path(self) -> None:
        sut = TransferReadyQueuePublisher()
        sut.publish_message(self.TEST_INGEST)

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

    def _get_expected_body(self) -> dict:
        return {
            'package_id': self.TEST_INGEST.package_id,
            's3_path': self.TEST_INGEST.s3_path,
            's3_bucket_name': self.TEST_INGEST.s3_bucket_name,
            'destination_path': os.getenv('INGEST_DESTINATION_PATH'),
            'admin_metadata': self.TEST_INGEST.admin_metadata,
            'application_name': self.TEST_INGEST.depositing_application.value
        }
