from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_failed_exception import \
    SetIngestAsTransferredFailedException
from app.ingest.domain.services.exceptions.transfer_status_message_handling_exception import \
    TransferStatusMessageHandlingException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.services.transfer_service import TransferService
from test.resources.ingest.ingest_factory import create_ingest


class TestTransferService(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id

        cls.TEST_TRANSFER_STATUS_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "successful"
        }

        cls.TEST_TRANSFER_STATUS_MESSAGE_FAILURE = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "failure"
        }

        cls.TEST_MESSAGE_ID = "test"

    def setUp(self) -> None:
        self.logger_mock = Mock(spec=Logger)

    def test_handle_transfer_status_message_successful_happy_path(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = TransferService(ingest_service_stub, self.logger_mock)
        sut.handle_transfer_status_message(
            self.TEST_TRANSFER_STATUS_MESSAGE_SUCCESSFUL,
            self.TEST_MESSAGE_ID
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_called_once_with(self.TEST_INGEST)

    def test_handle_transfer_status_message_successful_ingest_service_raises_get_ingest_by_package_id_exception(
            self
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.side_effect = GetIngestByPackageIdException("test", "test")

        sut = TransferService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(TransferStatusMessageHandlingException):
            sut.handle_transfer_status_message(
                self.TEST_TRANSFER_STATUS_MESSAGE_SUCCESSFUL,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_transfer_status_message_successful_service_raises_set_ingest_as_transferred_exception(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_transferred.side_effect = SetIngestAsTransferredException(
            "test",
            "test"
        )

        sut = TransferService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(TransferStatusMessageHandlingException):
            sut.handle_transfer_status_message(
                self.TEST_TRANSFER_STATUS_MESSAGE_SUCCESSFUL,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_transfer_status_message_successful_service_raises_process_ingest_exception(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.process_ingest.side_effect = ProcessIngestException("test", "test")

        sut = TransferService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(TransferStatusMessageHandlingException):
            sut.handle_transfer_status_message(
                self.TEST_TRANSFER_STATUS_MESSAGE_SUCCESSFUL,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_transferred.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.process_ingest.assert_called_once_with(self.TEST_INGEST)

    def test_handle_transfer_status_message_failure_happy_path(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = TransferService(ingest_service_stub, self.logger_mock)
        sut.handle_transfer_status_message(
            self.TEST_TRANSFER_STATUS_MESSAGE_FAILURE,
            self.TEST_MESSAGE_ID
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()

    def test_handle_transfer_status_message_failure_service_raises_set_ingest_as_transferred_failed_exception(
            self
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_transferred_failed.side_effect = SetIngestAsTransferredFailedException(
            "test",
            "test"
        )

        sut = TransferService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(TransferStatusMessageHandlingException):
            sut.handle_transfer_status_message(
                self.TEST_TRANSFER_STATUS_MESSAGE_FAILURE,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_transferred_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_transferred.assert_not_called()
        ingest_service_stub.process_ingest.assert_not_called()
