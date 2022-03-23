"""
This module defines an IngestCompletedQueueListener, which defines the necessary
logic to connect to a remote MQ and listen for ingestion completion messages.
"""
import os

import stomp
from stomp.utils import Frame

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from app.ingest.application.mq.stomp_interactor import StompInteractor


class IngestCompletedQueueListener(stomp.ConnectionListener, StompInteractor):

    def __init__(self) -> None:
        super().__init__()
        self.__mq_host = os.getenv('MQ_PROCESS_HOST')
        self.__mq_port = os.getenv('MQ_PROCESS_PORT')
        self.__ssl_enabled = os.getenv('MQ_PROCESS_SSL_ENABLED')
        self.__mq_user = os.getenv('MQ_PROCESS_USER')
        self.__mq_password = os.getenv('MQ_PROCESS_PASSWORD')
        self.__mq_queue_name = os.getenv('MQ_PROCESS_QUEUE')

        self.__reconnect_on_disconnection = True
        self.__connection = self.__create_subscribed_mq_connection()

    def on_message(self, frame: Frame) -> None:
        # TODO: Handle message and proper logging
        print("INFO: Received a MQ message: %s" % frame.body, flush=True)

    def on_error(self, frame: Frame) -> None:
        # TODO: Proper logging
        print("ERROR: Received a MQ error: %s" % frame.body, flush=True)

    def on_disconnected(self) -> None:
        if self.__reconnect_on_disconnection:
            self.reconnect()

    def reconnect(self) -> None:
        self.__reconnect_on_disconnection = True
        self.__connection = self.__create_subscribed_mq_connection()

    def disconnect(self) -> None:
        self.__reconnect_on_disconnection = False
        self.__connection.disconnect()

    def __create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection(
            MqConnectionParams(
                mq_host=self.__mq_host,
                mq_port=self.__mq_port,
                mq_ssl_enabled=self.__ssl_enabled,
                mq_user=self.__mq_user,
                mq_password=self.__mq_password
            )
        )

        connection.subscribe(destination=self.__mq_queue_name, id=1)
        connection.set_listener('', self)

        return connection
