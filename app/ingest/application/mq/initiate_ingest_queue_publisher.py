"""
This module defines an InitiateIngestQueuePublisher, an implementation of IInitiateIngestQueuePublisher
which includes the necessary logic to connect to a remote MQ and publish a message for ingestion initiation.
"""

import json
import os

import stomp

from app.ingest.domain.mq.exceptions.mq_connection_exception import MqConnectionException
from app.ingest.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher


class InitiateIngestQueuePublisher(IInitiateIngestQueuePublisher):
    __STOMP_CONN_HEARTBEATS_MS = 40000

    def __init__(self) -> None:
        self.__mq_host = os.getenv('MQ_HOST')
        self.__mq_port = os.getenv('MQ_PORT')
        self.__mq_queue_name = os.getenv('MQ_QUEUE')
        self.__mq_ssl_enabled = os.getenv('MQ_SSL_ENABLED')
        self.__mq_user = os.getenv('MQ_USER')
        self.__mq_password = os.getenv('MQ_PASSWORD')

    def publish_message(self) -> None:
        message_json = {}
        message_json_str = json.dumps(message_json)

        try:
            connection = self.__create_mq_connection()
        except Exception as e:
            raise MqConnectionException(
                queue_host=self.__mq_host,
                queue_port=self.__mq_port,
                reason=str(e)
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

    def __create_mq_connection(self) -> stomp.Connection:
        """
        Creates a stomp.Connection to MQ.
        """
        connection = stomp.Connection(
            host_and_ports=[(self.__mq_host, self.__mq_port)],
            heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
            keepalive=True
        )

        if self.__mq_ssl_enabled == 'True':
            connection.set_ssl([(self.__mq_host, self.__mq_port)])

        connection.connect(
            self.__mq_user,
            self.__mq_password,
            wait=True
        )

        return connection
