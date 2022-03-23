"""
This module defines an InitiateIngestQueuePublisher, an implementation of IInitiateIngestQueuePublisher
which includes the necessary logic to connect to a remote MQ and publish a message for ingestion initiation.
"""

import json
import os

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from app.ingest.application.mq.stomp_interactor import StompInteractor
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher


class InitiateIngestQueuePublisher(IInitiateIngestQueuePublisher, StompInteractor):

    def __init__(self) -> None:
        super().__init__()
        self.__mq_host = os.getenv('MQ_TRANSFER_HOST')
        self.__mq_port = os.getenv('MQ_TRANSFER_PORT')
        self.__mq_ssl_enabled = os.getenv('MQ_TRANSFER_SSL_ENABLED')
        self.__mq_user = os.getenv('MQ_TRANSFER_USER')
        self.__mq_password = os.getenv('MQ_TRANSFER_PASSWORD')
        self.__mq_queue_name = os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_READY')

    def publish_message(self, ingest: Ingest) -> None:
        message_json = self.__create_message_json(ingest)

        connection = self._create_mq_connection(
            MqConnectionParams(
                mq_host=self.__mq_host,
                mq_port=self.__mq_port,
                mq_ssl_enabled=self.__mq_ssl_enabled,
                mq_user=self.__mq_user,
                mq_password=self.__mq_password
            )
        )
        try:
            message_json_str = json.dumps(message_json)
            connection.send(self.__mq_queue_name, message_json_str)
        except Exception as e:
            raise MqMessagePublishException(
                queue_name=self.__mq_queue_name,
                queue_host=self.__mq_host,
                queue_port=self.__mq_port,
                reason=str(e)
            )

        connection.disconnect()

    def __create_message_json(self, ingest: Ingest) -> json:
        return {
            's3_path': ingest.s3_path,
            's3_bucket_name': ingest.s3_bucket_name,
            'dropbox_name': ingest.dropbox_name,
            'admin_metadata': ingest.admin_metadata,
        }
