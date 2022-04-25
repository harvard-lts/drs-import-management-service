"""
This module defines an ProcessStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for process status messages.
"""
import os

from stomp.utils import Frame

from app.common.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.containers import Services
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.ingest_service import IngestService


class ProcessStatusQueueListener(StompListenerBase):

    def __init__(self, ingest_service: IngestService = Services.ingest_service()) -> None:
        super().__init__()
        self.__ingest_service = ingest_service

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_PROCESS_QUEUE_PROCESS_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_PROCESS_HOST'),
            mq_port=os.getenv('MQ_PROCESS_PORT'),
            mq_ssl_enabled=os.getenv('MQ_PROCESS_SSL_ENABLED'),
            mq_user=os.getenv('MQ_PROCESS_USER'),
            mq_password=os.getenv('MQ_PROCESS_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict) -> None:
        self._logger.debug("Received message from Process Queue. Message body: " + str(message_body))
        # TODO Handle batch_ingest_status: Currently only considered successful

        package_id = message_body['package_id']
        self._logger.debug("Obtaining ingest by the package id of the received message " + package_id + "...")
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)
        except GetIngestByPackageIdException as e:
            self._logger.error(str(e))
            raise e

        self._logger.debug("Setting ingest as processed...")
        try:
            self.__ingest_service.set_ingest_as_processed(ingest)
        except SetIngestAsProcessedException as e:
            self._logger.error(str(e))
            raise e

    def _handle_received_error(self, frame: Frame) -> None:
        # TODO
        pass
