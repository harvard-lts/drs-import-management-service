"""
This module defines a ProcessReadyQueuePublisher, an implementation of IProcessReadyQueuePublisher
which includes the necessary logic to connect to the remote MQ and publish a process ready message.
"""

import os

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from app.ingest.application.mq.publishers.stomp_publisher_base import StompPublisherBase
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.process_ready_queue_publisher import IProcessReadyQueuePublisher


class ProcessReadyQueuePublisher(IProcessReadyQueuePublisher, StompPublisherBase):

    def publish_message(self, ingest: Ingest) -> None:
        message = self.__create_process_ready_message(ingest)
        self._publish_message(message)

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_PROCESS_READY')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )

    def __create_process_ready_message(self, ingest: Ingest) -> dict:
        return {
            'package_id': ingest.package_id,
            'destination_path': ingest.destination_path,
            'application_name': ingest.depositing_application.value
        }
