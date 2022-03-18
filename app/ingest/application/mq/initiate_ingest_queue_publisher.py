"""
This module defines an InitiateIngestQueuePublisher, an implementation of IInitiateIngestQueuePublisher
which includes the necessary logic to connect to a remote MQ and publish a message for ingestion initiation.
"""

import json
import os

from app.ingest.application.mq.stomp_interactor import StompInteractor
from app.ingest.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher
from app.ingest.application.mq.mq_connection_params import MqConnectionParams


class InitiateIngestQueuePublisher(IInitiateIngestQueuePublisher, StompInteractor):

    def __init__(self) -> None:
        super().__init__()
        self.__mq_host = os.getenv('MQ_HOST')
        self.__mq_port = os.getenv('MQ_PORT')
        self.__mq_user = os.getenv('MQ_USER')
        self.__mq_password = os.getenv('MQ_PASSWORD')
        self.__mq_queue_name = os.getenv('MQ_QUEUE')

    def publish_message(self) -> None:
        message_json = {}
        message_json_str = json.dumps(message_json)

        connection = self._create_mq_connection(
            MqConnectionParams(
                mq_host=self.__mq_host,
                mq_port=self.__mq_port,
                mq_user=self.__mq_user,
                mq_password=self.__mq_password
            )
        )
        try:
            connection.send(self.__mq_queue_name, message_json_str)
        except Exception as e:
            raise MqMessagePublishException(
                queue_name=self.__mq_queue_name,
                queue_host=self.__mq_host,
                queue_port=self.__mq_port,
                reason=str(e)
            )

        connection.disconnect()
