import json
import os

import stomp

from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher
from app.ingest.domain.mq.exceptions.mq_connection_exception import MqConnectionException
from app.ingest.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException


class InitiateIngestQueuePublisher(IInitiateIngestQueuePublisher):
    __MQ_HOST = os.getenv('MQ_HOST')
    __MQ_PORT = os.getenv('MQ_PORT')
    __MQ_QUEUE_NAME = os.getenv('MQ_QUEUE')

    __STOMP_CONN_HEARTBEATS_MS = 40000

    def publish_message(self) -> None:
        message_json = {}
        message_json_str = json.dumps(message_json)

        try:
            connection = self.__create_mq_connection()
        except Exception as e:
            raise MqConnectionException(
                queue_host=self.__MQ_HOST,
                queue_port=self.__MQ_PORT,
                reason=str(e)
            )

        try:
            connection.send(self.__MQ_QUEUE_NAME, message_json_str)
        except Exception as e:
            raise MqMessagePublishException(
                queue_name=self.__MQ_QUEUE_NAME,
                queue_host=self.__MQ_HOST,
                queue_port=self.__MQ_PORT,
                reason=str(e)
            )

    def __create_mq_connection(self) -> stomp.Connection:
        connection = stomp.Connection(
            host_and_ports=[(self.__MQ_HOST, self.__MQ_PORT)],
            heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
            keepalive=True
        )

        if os.getenv('MQ_SSL_ENABLED') == 'True':
            connection.set_ssl([(self.__MQ_HOST, self.__MQ_PORT)])

        connection.connect(
            os.getenv('MQ_USER'),
            os.getenv('MQ_PASSWORD'),
            wait=True
        )

        return connection
