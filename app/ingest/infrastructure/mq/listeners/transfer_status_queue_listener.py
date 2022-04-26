"""
This module defines a TransferStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for transfer status messages.
"""
import os

from stomp.utils import Frame

from app.common.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.containers import Services
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.ingest_service import IngestService


class TransferStatusQueueListener(StompListenerBase):

    def __init__(self, ingest_service: IngestService = Services.ingest_service()) -> None:
        super().__init__()
        self.__ingest_service = ingest_service

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_TRANSFER_HOST'),
            mq_port=os.getenv('MQ_TRANSFER_PORT'),
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict) -> None:
        self._logger.debug("Received message from Transfer Queue. Message body: " + str(message_body))

        package_id = message_body['package_id']
        self._logger.debug("Obtaining ingest by the package id of the received message " + package_id + "...")
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)
        except GetIngestByPackageIdException as e:
            self._logger.error(str(e))
            raise e

        transfer_status = message_body['transfer_status']
        if transfer_status == "failure":
            self._logger.debug("Setting ingest as transferred failed...")
            self.__ingest_service.set_ingest_as_transferred_failed(ingest)
            return

        self._logger.debug("Setting ingest as transferred...")
        try:
            self.__ingest_service.set_ingest_as_transferred(ingest, message_body['destination_path'])
        except SetIngestAsTransferredException as e:
            self._logger.error(str(e))
            raise e

        self._logger.debug("Starting ingest processing...")
        try:
            self.__ingest_service.process_ingest(ingest)
        except ProcessIngestException as e:
            self._logger.error(str(e))
            raise e

    def _handle_received_error(self, frame: Frame) -> None:
        # TODO Handle error
        pass
