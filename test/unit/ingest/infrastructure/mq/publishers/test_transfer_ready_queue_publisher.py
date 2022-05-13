from unittest import TestCase
from unittest.mock import patch

from app.ingest.infrastructure.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from test.resources.ingest.ingest_factory import create_ingest


class TestTransferReadyQueuePublisher(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_DESTINATION_PATH = "test_path"

    @patch("app.common.infrastructure.mq.publishers.stomp_publisher_base.StompPublisherBase._publish_message")
    @patch('app.ingest.infrastructure.mq.publishers.transfer_ready_queue_publisher.os.getenv')
    def test_publish_message_happy_path(self, os_getenv_stub, inner_publish_message_mock) -> None:
        os_getenv_stub.return_value = self.TEST_DESTINATION_PATH

        self.sut = TransferReadyQueuePublisher()
        self.sut.publish_message(self.TEST_INGEST)

        inner_publish_message_mock.assert_called_once_with(
            {
                'package_id': self.TEST_INGEST.package_id,
                's3_path': self.TEST_INGEST.s3_path,
                's3_bucket_name': self.TEST_INGEST.s3_bucket_name,
                'destination_path': self.TEST_DESTINATION_PATH,
                'admin_metadata': self.TEST_INGEST.admin_metadata,
            }
        )
