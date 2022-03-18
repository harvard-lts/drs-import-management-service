import os
from abc import ABC

import stomp

from app.ingest.domain.mq.exceptions.mq_connection_exception import MqConnectionException


class StompInteractor(ABC):
    __STOMP_CONN_HEARTBEATS_MS = 40000

    def __init__(self) -> None:
        self._mq_host = os.getenv('MQ_HOST')
        self._mq_port = os.getenv('MQ_PORT')
        self._mq_user = os.getenv('MQ_USER')
        self._mq_password = os.getenv('MQ_PASSWORD')
        self.__mq_ssl_enabled = os.getenv('MQ_SSL_ENABLED')

    def _create_mq_connection(self) -> stomp.Connection:
        """
        Creates a stomp.Connection to MQ.
        """
        try:
            connection = stomp.Connection(
                host_and_ports=[(self._mq_host, self._mq_port)],
                heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
                keepalive=True
            )

            if self.__mq_ssl_enabled == 'True':
                connection.set_ssl([(self.__mq_host, self.__mq_port)])

            connection.connect(
                self._mq_user,
                self._mq_password,
                wait=True
            )

            return connection
        except Exception as e:
            raise MqConnectionException(
                queue_host=self._mq_host,
                queue_port=self._mq_port,
                reason=str(e)
            )
