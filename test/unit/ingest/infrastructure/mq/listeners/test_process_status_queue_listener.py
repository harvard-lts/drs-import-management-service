from unittest import TestCase
from unittest.mock import patch, Mock

from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.infrastructure.mq.listeners.process_status_queue_listener import ProcessStatusQueueListener
from test.resources.ingest.ingest_factory import create_ingest


class TestProcessStatusQueueListener(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id
        cls.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "successful",
            "message": "test"
        }

    @patch(
        "app.common.infrastructure.mq.listeners.stomp_listener_base.StompListenerBase"
        "._StompListenerBase__create_subscribed_mq_connection"
    )
    def test_handle_received_message_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        self.sut = ProcessStatusQueueListener(ingest_service_stub)

        self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with("test_package_id")
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(self.TEST_INGEST)
