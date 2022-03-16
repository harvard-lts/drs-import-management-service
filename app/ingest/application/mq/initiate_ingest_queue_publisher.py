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

    def __create_mq_connection(self) -> stomp.Connection:
        connection = stomp.Connection(
            host_and_ports=[(self.__mq_host, self.__mq_port)],
            heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
            keepalive=True
        )

        if os.getenv('MQ_SSL_ENABLED') == 'True':
            connection.set_ssl([(self.__mq_host, self.__mq_port)])

        connection.connect(
            os.getenv('MQ_USER'),
            os.getenv('MQ_PASSWORD'),
            wait=True
        )

        return connection
