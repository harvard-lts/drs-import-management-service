from unittest import TestCase
from unittest.mock import patch, Mock

from app.ingest.application.mq.listeners.transfer_status_queue_listener import TransferStatusQueueListener
from app.ingest.domain.services.ingest_service import IngestService
from test.resources.ingest.ingest_factory import create_ingest


class TestTransferStatusQueueListener(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id
        cls.TEST_DESTINATION_PATH = "test_destination_path"
        cls.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "successful",
            "destination_path": cls.TEST_DESTINATION_PATH
        }

    @patch(
        "app.ingest.application.mq.listeners.stomp_listener_base.StompListenerBase"
        "._StompListenerBase__create_subscribed_mq_connection"
    )
    def test_handle_received_message_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        self.sut = TransferStatusQueueListener(ingest_service_stub)

        self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST,
                                                                              self.TEST_DESTINATION_PATH)
        ingest_service_stub.process_ingest.assert_called_once_with(self.TEST_INGEST)
