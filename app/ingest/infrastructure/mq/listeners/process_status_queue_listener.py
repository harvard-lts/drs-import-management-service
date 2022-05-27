"""
This module defines an ProcessStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for process status messages.
"""
import os

from app.common.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.containers import Services
from app.ingest.domain.services.exceptions.process_service_exception import ProcessServiceException
from app.ingest.domain.services.process_service import ProcessService


class ProcessStatusQueueListener(StompListenerBase):

    def __init__(self, process_service: ProcessService = Services.process_service()) -> None:
        super().__init__()
        self.__process_service = process_service

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_PROCESS_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        self._logger.info(
            "Received message from Process Queue. Message body: {}. Message id: {}".format(
                str(message_body),
                message_id
            )
        )
        try:
            self.__process_service.handle_process_status_message(message_body, message_id)
            self._acknowledge_message(message_id, message_subscription)
        except ProcessServiceException as e:
            self._logger.error(str(e))
            self._unacknowledge_message(message_id, message_subscription)
