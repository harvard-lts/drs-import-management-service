import os
import time

import stomp

from test.integration.integration_test_base import IntegrationTestBase


class StompIntegrationTestBase(IntegrationTestBase):
    __STOMP_CONN_HEARTBEATS_MS = 40000
    __MESSAGE_AWAIT_TIMEOUT_SECONDS = 30

    def _create_mq_connection(self) -> stomp.Connection:
        mq_host = os.getenv('MQ_HOST')
        mq_port = os.getenv('MQ_PORT')
        mq_ssl_enabled = os.getenv('MQ_SSL_ENABLED')
        mq_user = os.getenv('MQ_USER')
        mq_password = os.getenv('MQ_PASSWORD')

        connection = stomp.Connection(
            host_and_ports=[(mq_host, mq_port)],
            heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
            keepalive=True
        )

        if os.getenv(mq_ssl_enabled) == 'True':
            connection.set_ssl([(mq_host, mq_port)])

        connection.connect(
            mq_user,
            mq_password,
            wait=True
        )

        return connection

    def _get_message_await_timeout(self) -> float:
        return time.time() + self.__MESSAGE_AWAIT_TIMEOUT_SECONDS
