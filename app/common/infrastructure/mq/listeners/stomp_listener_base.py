"""
This module defines a StompListenerBase, which is an abstract class intended
to define common behavior for stomp-implemented MQ listener components.
"""
import json
from abc import abstractmethod, ABC

import stomp
from stomp.utils import Frame

from app.common.infrastructure.mq.stomp_interactor import StompInteractor


class StompListenerBase(stomp.ConnectionListener, StompInteractor, ABC):

    def __init__(self) -> None:
        self.__reconnect_on_disconnection = True
        self.__connection = self.__create_subscribed_mq_connection()

    def on_message(self, frame: Frame) -> None:
        try:
            message_body = json.loads(frame.body)
        except json.decoder.JSONDecodeError as e:
            # TODO Handle exception
            raise e

        self._handle_received_message(message_body)

    def on_error(self, frame: Frame) -> None:
        self._handle_received_error(frame)

    def on_disconnected(self) -> None:
        if self.__reconnect_on_disconnection:
            self.reconnect()

    def reconnect(self) -> None:
        self.__reconnect_on_disconnection = True
        self.__connection = self.__create_subscribed_mq_connection()

    def disconnect(self) -> None:
        self.__reconnect_on_disconnection = False
        self.__connection.disconnect()

    @abstractmethod
    def _handle_received_message(self, message_body: dict) -> None:
        """
        Handles the received message by adding child listener specific logic.

        :param message_body: received message body
        :type message_body: dict
        """

    @abstractmethod
    def _handle_received_error(self, frame: Frame) -> None:
        """
        Handles the received error by adding child listener specific logic.

        :param frame: received stomp error Frame
        :type frame: stomp.utils.Frame
        """

    def __create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection()
        connection.subscribe(destination=self._get_queue_name(), id=1)
        connection.set_listener('', self)
        return connection
