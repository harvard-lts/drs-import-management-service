import os
from abc import ABC

import stomp

from app.ingest.domain.mq.exceptions.mq_connection_exception import MqConnectionException
from app.ingest.application.mq.mq_connection_params import MqConnectionParams


class StompInteractor(ABC):
    __STOMP_CONN_HEARTBEATS_MS = 40000

    def __init__(self) -> None:
        self.__mq_ssl_enabled = os.getenv('MQ_SSL_ENABLED')

    def _create_mq_connection(self, mq_connection_params: MqConnectionParams) -> stomp.Connection:
        """
        Creates a stomp.Connection to MQ.

        :param mq_connection_params: MQ connection parameters
        :type mq_connection_params: MqConnectionParams
        """
        try:
            connection = stomp.Connection(
                host_and_ports=[(mq_connection_params.mq_host, mq_connection_params.mq_port)],
                heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
                keepalive=True
            )

            if self.__mq_ssl_enabled == 'True':
                connection.set_ssl([(mq_connection_params.mq_host, mq_connection_params.mq_port)])

            connection.connect(
                mq_connection_params.mq_user,
                mq_connection_params.mq_password,
                wait=True
            )

            return connection

        except Exception as e:
            raise MqConnectionException(
                queue_host=mq_connection_params.mq_host,
                queue_port=mq_connection_params.mq_port,
                reason=str(e)
            )
