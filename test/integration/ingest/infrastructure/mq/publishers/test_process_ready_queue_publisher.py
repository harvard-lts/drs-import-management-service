import os

from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.ingest.infrastructure.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from test.integration.common.infrastructure.mq.publishers.stomp_publisher_integration_test_base import \
    StompPublisherIntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestProcessReadyQueuePublisher(StompPublisherIntegrationTestBase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()

    def test_publish_message_happy_path(self) -> None:
        sut = ProcessReadyQueuePublisher()
        sut.publish_message(self.TEST_INGEST)

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

    def _get_expected_body(self) -> dict:
        base_dropbox_path = os.getenv('BASE_DROPBOX_PATH')

        return {
            'package_id': self.TEST_INGEST.package_id,
            'destination_path': os.path.join(base_dropbox_path, os.getenv('DATAVERSE_DROPBOX_NAME'), "incoming"),
            'application_name': self.TEST_INGEST.depositing_application,
            'admin_metadata':
                self.TEST_INGEST.admin_metadata | {'original_queue': self._get_queue_name(), 'retry_count': 0}
        }
