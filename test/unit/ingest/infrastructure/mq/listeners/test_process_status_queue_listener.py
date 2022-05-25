from unittest import TestCase
from unittest.mock import patch, Mock

from stomp import Connection

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

        cls.TEST_MESSAGE_ID = "test"

        cls.TEST_MESSAGE_SUBSCRIPTION = "test"

    def setUp(self) -> None:
        self.connection_mock = Mock(spec=Connection)

    def test_handle_received_message_successful_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = ProcessStatusQueueListener(ingest_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with("test_package_id")
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL["drs_url"]
        )
        self.connection_mock.ack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
        self.connection_mock.nack.assert_not_called()

    def test_handle_received_message_successful_service_raises_get_ingest_by_package_id_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.side_effect = GetIngestByPackageIdException("test", "test")

        sut = ProcessStatusQueueListener(ingest_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_not_called()
        self.connection_mock.ack.assert_not_called()
        self.connection_mock.nack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )

    def test_handle_received_message_successful_service_raises_set_ingest_as_processed_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed.side_effect = SetIngestAsProcessedException(
            "test",
            "test"
        )

        sut = ProcessStatusQueueListener(ingest_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_not_called()
        ingest_service_stub.set_ingest_as_processed.assert_called_once_with(
            self.TEST_INGEST,
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_SUCCESSFUL["drs_url"]
        )
        self.connection_mock.ack.assert_not_called()
        self.connection_mock.nack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )

    def test_handle_received_message_failure_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST

        sut = ProcessStatusQueueListener(ingest_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_FAILURE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()
        self.connection_mock.ack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
        self.connection_mock.nack.assert_not_called()

    def test_handle_received_message_failure_service_raises_set_ingest_as_processed_failed_exception(
            self,
            create_subscribed_mq_connection_mock
    ) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        ingest_service_stub = Mock(spec=IngestService)
        ingest_service_stub.get_ingest_by_package_id.return_value = self.TEST_INGEST
        ingest_service_stub.set_ingest_as_processed_failed.side_effect = SetIngestAsProcessedFailedException(
            "test",
            "test"
        )

        sut = ProcessStatusQueueListener(ingest_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_RECEIVED_MESSAGE_FAILURE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        ingest_service_stub.get_ingest_by_package_id.assert_called_once_with(self.TEST_PACKAGE_ID)
        ingest_service_stub.set_ingest_as_processed_failed.assert_called_once_with(self.TEST_INGEST)
        ingest_service_stub.set_ingest_as_processed.assert_not_called()
        self.connection_mock.ack.assert_not_called()
        self.connection_mock.nack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
