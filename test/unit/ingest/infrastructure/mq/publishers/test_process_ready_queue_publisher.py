from unittest import TestCase
from unittest.mock import patch

from app.ingest.infrastructure.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from test.resources.ingest.ingest_factory import create_ingest


class TestProcessReadyQueuePublisher(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_DESTINATION_PATH = "test_path"

    @patch("app.common.infrastructure.mq.publishers.stomp_publisher_base.StompPublisherBase._publish_message")
    @patch('app.ingest.infrastructure.mq.publishers.process_ready_queue_publisher.os.getenv')
    def test_publish_message_happy_path(self, os_getenv_stub, inner_publish_message_mock) -> None:
        os_getenv_stub.return_value = self.TEST_DESTINATION_PATH

        self.sut = ProcessReadyQueuePublisher()
        self.sut.publish_message(self.TEST_INGEST)

        inner_publish_message_mock.assert_called_once_with(
            {
                'package_id': self.TEST_INGEST.package_id,
                'destination_path': self.TEST_DESTINATION_PATH + "/" + self.TEST_DESTINATION_PATH + "/incoming",
                'admin_metadata': self.TEST_INGEST.admin_metadata,
                'application_name': self.TEST_INGEST.depositing_application
            }
        )
