from unittest import TestCase
from unittest.mock import patch, Mock

from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_failed_exception import \
    SetIngestAsProcessedFailedException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.infrastructure.mq.listeners.process_status_queue_listener import ProcessStatusQueueListener
from test.resources.ingest.ingest_factory import create_ingest


@patch(
    "app.common.infrastructure.mq.listeners.stomp_listener_base.StompListenerBase"
    "._StompListenerBase__create_subscribed_mq_connection"
)
class TestProcessStatusQueueListener(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.TEST_PACKAGE_ID = cls.TEST_INGEST.package_id

        cls.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "successful",
            "drs_url": "test",
            "message": "test"
        }

        cls.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_FAILURE = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "failure",
            "message": "test"
        }

    def test_handle_received_message_successful_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        self.sut = ProcessStatusQueueListener(ingest_service_stub)

        self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with("test_package_id")
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL["drs_url"]
        )

    def test_handle_received_message_successful_service_raises_get_ingest_by_package_id_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.side_effect = GetIngestByPackageIdException("test", "test")

        self.sut = ProcessStatusQueueListener(ingest_service_stub)
        with self.assertRaises(GetIngestByPackageIdException):
            self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_not_called()

    def test_handle_received_message_successful_service_raises_set_ingest_as_processed_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed.side_effect = SetIngestAsProcessedException(
            "test",
            "test"
        )

        self.sut = ProcessStatusQueueListener(ingest_service_stub)
        with self.assertRaises(SetIngestAsProcessedException):
            self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL["drs_url"]
        )

    def test_handle_received_message_failure_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        self.sut = ProcessStatusQueueListener(ingest_service_stub)
        self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_FAILURE)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()

    def test_handle_received_message_failure_service_raises_set_ingest_as_processed_failed_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed_failed.side_effect = SetIngestAsProcessedFailedException(
            "test",
            "test"
        )

        self.sut = ProcessStatusQueueListener(ingest_service_stub)
        with self.assertRaises(SetIngestAsProcessedFailedException):
            self.sut._handle_received_message(self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_FAILURE)

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()
