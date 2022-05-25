from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_status_message_handling_exception import \
    ProcessStatusMessageHandlingException
from app.ingest.domain.services.exceptions.process_status_message_missing_field_exception import \
    ProcessStatusMessageMissingFieldException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_failed_exception import \
    SetIngestAsProcessedFailedException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.services.process_service import ProcessService
from test.resources.ingest.ingest_factory import create_ingest


class TestProcessService(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id

        cls.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "successful",
            "drs_url": "test",
            "message": "test"
        }

        cls.TEST_PROCESS_STATUS_MESSAGE_FAILURE = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "failure",
            "drs_url": "test",
            "message": "test"
        }

        cls.TEST_PROCESS_MESSAGE_MISSING_FIELD = {
            "application_name": cls.TEST_INGEST.depositing_application
        }

        cls.TEST_MESSAGE_ID = "test"

    def setUp(self) -> None:
        self.logger_mock = Mock(spec=Logger)

    def test_handle_process_status_message_successful_happy_path(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = ProcessService(ingest_service_stub, self.logger_mock)
        sut.handle_process_status_message(
            self.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL,
            self.TEST_MESSAGE_ID
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with("test_package_id")
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL["drs_url"]
        )

    def test_handle_process_status_message_successful_service_raises_get_ingest_by_package_id_exception(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.side_effect = GetIngestByPackageIdException("test", "test")

        sut = ProcessService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(ProcessStatusMessageHandlingException):
            sut.handle_process_status_message(
                self.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_not_called()

    def test_handle_process_status_message_successful_service_raises_set_ingest_as_processed_exception(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed.side_effect = SetIngestAsProcessedException("test", "test")

        sut = ProcessService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(ProcessStatusMessageHandlingException):
            sut.handle_process_status_message(
                self.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_MESSAGE_SUCCESSFUL["drs_url"]
        )

    def test_handle_process_status_message_failure_happy_path(self) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = ProcessService(ingest_service_stub, self.logger_mock)
        sut.handle_process_status_message(
            self.TEST_PROCESS_STATUS_MESSAGE_FAILURE,
            self.TEST_MESSAGE_ID
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()

    def test_handle_process_status_message_failure_service_raises_set_ingest_as_processed_failed_exception(
            self
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed_failed.side_effect = SetIngestAsProcessedFailedException(
            "test",
            "test"
        )

        sut = ProcessService(ingest_service_stub, self.logger_mock)
        with self.assertRaises(ProcessStatusMessageHandlingException):
            sut.handle_process_status_message(
                self.TEST_PROCESS_STATUS_MESSAGE_FAILURE,
                self.TEST_MESSAGE_ID
            )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()

    def test_handle_process_status_message_missing_message_field(self) -> None:
        ingest_service_mock = Mock(spec=IngestService)
        ingest_service_mock.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = ProcessService(ingest_service_mock, self.logger_mock)
        with self.assertRaises(ProcessStatusMessageMissingFieldException):
            sut.handle_process_status_message(
                self.TEST_PROCESS_MESSAGE_MISSING_FIELD,
                self.TEST_MESSAGE_ID
            )

        ingest_service_mock.get_ingest_by_package_id.assert_not_called()
        ingest_service_mock.set_ingest_as_transferred_failed.assert_not_called()
        ingest_service_mock.set_ingest_as_transferred.assert_not_called()
        ingest_service_mock.process_ingest.assert_not_called()
