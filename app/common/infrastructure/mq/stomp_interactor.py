"""
This module defines a StompInteractor, which is an abstract class intended
to define common behavior for stomp-implemented MQ components.
"""

from abc import ABC, abstractmethod

import stomp

from app.ingest.domain.mq.exceptions.mq_connection_exception import MqConnectionException
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams


class StompInteractor(ABC):
    __STOMP_CONN_HEARTBEATS_MS = 40000

    def _create_mq_connection(self) -> stomp.Connection:
        """
        Creates a stomp.Connection to MQ.
        """
        mq_connection_params = self._get_mq_connection_params()

        mq_host = mq_connection_params.mq_host
        mq_port = mq_connection_params.mq_port
        #mq_ssl_enabled = mq_connection_params.mq_ssl_enabled
        mq_user = mq_connection_params.mq_user
        mq_password = mq_connection_params.mq_password

        try:
            connection = stomp.Connection(
                host_and_ports=[(mq_host, mq_port)],
                heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
                keepalive=True
            )

            #if mq_ssl_enabled == 'True':
            connection.set_ssl([(mq_host, mq_port)])

            connection.connect(
                mq_user,
                mq_password,
                wait=True
            )

            return connection

        except Exception as e:
            raise MqConnectionException(
                queue_host=mq_host,
                queue_port=mq_port,
                reason=str(e)
            )

    @abstractmethod
    def _get_mq_connection_params(self) -> MqConnectionParams:
        """
        Retrieves the MQ connection params necessary for creating the connection
        """

    @abstractmethod
    def _get_queue_name(self) -> str:
        """
        Retrieves the name of the queue to be interacted with
        """
