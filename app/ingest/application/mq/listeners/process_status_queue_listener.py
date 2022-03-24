"""
This module defines an ProcessStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for process status messages.
"""
import os

from stomp.utils import Frame

from app.ingest.application.mq.listeners.stomp_listener_base import StompListenerBase
from app.ingest.application.mq.mq_connection_params import MqConnectionParams


class ProcessStatusQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_DRS_INGEST_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )

    def _handle_received_message(self, frame: Frame) -> None:
        pass

    def _handle_received_error(self, frame: Frame) -> None:
        pass
