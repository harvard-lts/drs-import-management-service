"""
This module defines a TransferStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for transfer status messages.
"""
import os, traceback

from app.common.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.containers import Services
from app.ingest.domain.services.exceptions.transfer_service_exception import TransferServiceException
from app.ingest.domain.services.transfer_service import TransferService
import app.notifier.notifier as notifier


class TransferStatusQueueListener(StompListenerBase):

    def __init__(self, transfer_service: TransferService = Services.transfer_service()) -> None:
        super().__init__()
        self.__transfer_service = transfer_service

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_TRANSFER_HOST'),
            mq_port=os.getenv('MQ_TRANSFER_PORT'),
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        self._logger.info(
            "Received message from Transfer Queue. Message body: {}. Message id: {}".format(
                str(message_body),
                message_id
            )
        )
        try:
            self.__transfer_service.handle_transfer_status_message(message_body, message_id)
            self._acknowledge_message(message_id, message_subscription)
        except TransferServiceException as e:
            msg = "Could not transfer ingest for {}.  Error {}.".format(str(message_body), str(e))
            exception_msg = traceback.format_exc()
            body = msg + "\n" + exception_msg
            notifier.send_error_notification(str(e), body)
            
            self._unacknowledge_message(message_id, message_subscription)
