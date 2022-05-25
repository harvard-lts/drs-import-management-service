from unittest import TestCase
from unittest.mock import patch, Mock

from stomp import Connection

from app.ingest.domain.services.exceptions.transfer_service_exception import TransferServiceException
from app.ingest.domain.services.transfer_service import TransferService
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

        cls.TEST_TRANSFER_STATUS_MESSAGE = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "successful"
        }

        cls.TEST_TRANSFER_STATUS_RECEIVED_MESSAGE_FAILURE = {
            "package_id": cls.TEST_PACKAGE_ID,
            "transfer_status": "failure"
        }

        cls.TEST_MESSAGE_ID = "test"

        cls.TEST_MESSAGE_SUBSCRIPTION = "test"

    def setUp(self) -> None:
        self.connection_mock = Mock(spec=Connection)

    def test_handle_received_message_successful_happy_path(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        transfer_service_mock = Mock(spec=TransferService)

        sut = TransferStatusQueueListener(transfer_service_mock)
        sut._handle_received_message(
            self.TEST_TRANSFER_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        transfer_service_mock.handle_transfer_status_message.assert_called_once_with(
            self.TEST_TRANSFER_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID
        )
        self.connection_mock.ack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
        self.connection_mock.nack.assert_not_called()

    def test_handle_received_message_service_raises_exception(self, create_subscribed_mq_connection_mock) -> None:
        create_subscribed_mq_connection_mock.return_value = self.connection_mock
        transfer_service_stub = Mock(spec=TransferService)
        transfer_service_stub.handle_transfer_status_message.side_effect = TransferServiceException()

        sut = TransferStatusQueueListener(transfer_service_stub)
        sut._handle_received_message(
            self.TEST_TRANSFER_STATUS_MESSAGE,
            self.TEST_MESSAGE_ID,
            self.TEST_MESSAGE_SUBSCRIPTION
        )

        self.connection_mock.ack.assert_not_called()
        self.connection_mock.nack.assert_called_once_with(
            id=self.TEST_MESSAGE_ID,
            subscription=self.TEST_MESSAGE_SUBSCRIPTION
        )
