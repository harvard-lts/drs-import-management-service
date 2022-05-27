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
    __ACK_CLIENT_INDIVIDUAL = "client-individual"

    def __init__(self) -> None:
        super().__init__()
        self.__reconnect_on_disconnection = True
        self._connection = self.__create_subscribed_mq_connection()

    def on_message(self, frame: Frame) -> None:
        message_id = frame.headers['message-id']
        message_subscription = frame.headers['subscription']
        try:
            message_body = json.loads(frame.body)
            self._handle_received_message(message_body, message_id, message_subscription)
        except json.decoder.JSONDecodeError as e:
            self._logger.error(str(e))
            self._unacknowledge_message(message_id, message_subscription)

    def on_error(self, frame: Frame) -> None:
        self._logger.info("MQ error received: " + frame.body)

    def on_disconnected(self) -> None:
        self._logger.debug("Disconnected from MQ")
        if self.__reconnect_on_disconnection:
            self._logger.debug("Reconnecting to MQ...")
            self.reconnect()

    def reconnect(self) -> None:
        self.__reconnect_on_disconnection = True
        self._connection = self.__create_subscribed_mq_connection()

    def disconnect(self) -> None:
        self.__reconnect_on_disconnection = False
        self._connection.disconnect()

    @abstractmethod
    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        """
        Handles the received message by adding child listener specific logic.

        :param message_body: received message body
        :type message_body: dict
        :param message_id: received message id
        :type message_id: str
        :param message_subscription: received message subscription
        :type message_subscription: str
        """

    def _acknowledge_message(self, message_id: str, message_subscription: str) -> None:
        """
        Informs the MQ that the message was consumed

        :param message_id: message id
        :type message_id: str
        :param message_subscription: message subscription
        :type message_subscription: str
        """
        self._logger.info("Setting message with id {} as acknowledged...".format(message_id))
        self._connection.ack(id=message_id, subscription=message_subscription)

    def _unacknowledge_message(self, message_id: str, message_subscription: str) -> None:
        """
        Informs the MQ that the message was not consumed

        :param message_id: message id
        :type message_id: str
        :param message_subscription: message subscription
        :type message_subscription: str
        """
        self._logger.info("Setting message with id {} as unacknowledged...".format(message_id))
        self._connection.nack(id=message_id, subscription=message_subscription)

    def __create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection()
        connection.subscribe(destination=self._get_queue_name(), id=1, ack=self.__ACK_CLIENT_INDIVIDUAL)
        connection.set_listener('', self)
        return connection
