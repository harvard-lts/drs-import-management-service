from unittest import TestCase
from unittest.mock import patch, Mock

from stomp import Connection

from app.ingest.domain.services.exceptions.process_service_exception import ProcessServiceException
from app.ingest.domain.services.process_service import ProcessService
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

        cls.TEST_PROCESS_STATUS_MESSAGE = {
            "package_id": cls.TEST_INGEST.package_id,
            "application_name": cls.TEST_INGEST.depositing_application,
            "batch_ingest_status": "successful",
            "drs_url": "test",
            "message": "test"
        }

        cls.TEST_MESSAGE_ID = "test"

        cls.TEST_MESSAGE_SUBSCRIPTION = "test"

    def setUp(self) -> None:
        self.connection_mock = Mock(spec=Connection)

    def test_handle_received_message_successful_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        process_service_mock = Mock(spec=ProcessService)

        sut = ProcessStatusQueueListener(process_service_mock)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        process_service_mock.handle_process_status_message.assert_called_once_with(
            self.TEST_PROCESS_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID
        )
        self.connection_mock.ack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
        self.connection_mock.nack.assert_not_called()

    def test_handle_received_message_service_raises_exception(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        process_service_stub = Mock(spec=ProcessService)
        process_service_stub.handle_process_status_message.side_effect = ProcessServiceException()

        sut = ProcessStatusQueueListener(process_service_stub)
        sut._handle_received_message(
            self.TEST_PROCESS_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        self.connection_mock.ack.assert_not_called()
        self.connection_mock.nack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
