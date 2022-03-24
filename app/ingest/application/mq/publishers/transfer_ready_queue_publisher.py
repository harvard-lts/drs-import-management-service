"""
This module defines a TransferReadyQueuePublisher, an implementation of ITransferReadyQueuePublisher
which includes the necessary logic to connect to the remote MQ and publish a transfer ready message.
"""

import json
import os

from app.ingest.application.mq.stomp_interactor import StompInteractor
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.ingest.domain.mq.transfer_ready_queue_publisher import ITransferReadyQueuePublisher
from app.ingest.application.mq.mq_connection_params import MqConnectionParams


class TransferReadyQueuePublisher(ITransferReadyQueuePublisher, StompInteractor):

    def __init__(self) -> None:
        self.__mq_host = os.getenv('MQ_TRANSFER_HOST')
        self.__mq_port = os.getenv('MQ_TRANSFER_PORT')

    def publish_message(self, ingest: Ingest) -> None:
        message_json = self.__create_message_json(ingest)

        connection = self._create_mq_connection()
        try:
            message_json_str = json.dumps(message_json)
            connection.send(self._get_queue_name(), message_json_str)
        except Exception as e:
            raise MqMessagePublishException(
                queue_name=self._get_queue_name(),
                queue_host=self.__mq_host,
                queue_port=self.__mq_port,
                reason=str(e)
            )

        connection.disconnect()

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_READY')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=self.__mq_host,
            mq_port=self.__mq_port,
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def __create_message_json(self, ingest: Ingest) -> json:
        return {
            's3_path': ingest.s3_path,
            's3_bucket_name': ingest.s3_bucket_name,
            'dropbox_name': ingest.dropbox_name,
            'admin_metadata': ingest.admin_metadata,
        }
