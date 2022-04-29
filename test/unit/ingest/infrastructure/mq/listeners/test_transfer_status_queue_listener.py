from unittest import TestCase
from unittest.mock import patch, Mock

from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_failed_exception import \
    SetIngestAsTransferredFailedException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.infrastructure.mq.listeners.transfer_status_queue_listener import TransferStatusQueueListener
from test.resources.ingest.ingest_factory import create_ingest


@patch(
    "app.common.infrastructure.mq.listeners.stomp_listener_base.StompListenerBase"
    "._StompListenerBase__create_subscribed_mq_connection"
)
class TestTransferStatusQueueListener(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id

        cls.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "successful"
        }

        cls.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_FAILURE = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "failure"
        }

    def test_handle_received_message_successful_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_called_once_with(self.TEST_INGEST)

    def test_handle_received_message_successful_service_raises_get_ingest_by_package_id_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.side_effect = GetIngestByPackageIdException("test", "test")

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        with self.assertRaises(GetIngestByPackageIdException):
            self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_received_message_successful_service_raises_set_ingest_as_transferred_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_transferred.side_effect = SetIngestAsTransferredException(
            "test",
            "test"
        )

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        with self.assertRaises(SetIngestAsTransferredException):
            self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_received_message_successful_service_raises_process_ingest_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.process_ingest.side_effect = ProcessIngestException("test", "test")

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        with self.assertRaises(ProcessIngestException):
            self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_called_once_with(self.TEST_INGEST)

    def test_handle_received_message_failure_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_FAILURE)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_received_message_failure_service_raises_set_ingest_as_transferred_failed_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_transferred_failed.side_effect = SetIngestAsTransferredFailedException(
            "test",
            "test"
        )

        self.sut = TransferStatusQueueListener(ingest_service_stub)
        with self.assertRaises(SetIngestAsTransferredFailedException):
            self.sut._handle_received_message(self.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_FAILURE)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()
