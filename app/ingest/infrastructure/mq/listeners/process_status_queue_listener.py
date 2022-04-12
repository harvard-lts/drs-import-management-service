"""
This module defines an ProcessStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for process status messages.
"""
import os

from stomp.utils import Frame

from app.containers import Services
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.ingest.infrastructure.mq.mq_connection_params import MqConnectionParams


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
        # TODO Handle batch_ingest_status: Currently only considered successful

        # TODO Fake ingest until MongoDB persistence is implemented
        # https://github.com/harvard-lts/HDC/issues/104
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(message_body['package_id'])
        except GetIngestByPackageIdException as e:
            # TODO Handle exception
            raise e

        try:
            self.__ingest_service.set_ingest_as_processed(ingest)
        except SetIngestAsProcessedException as e:
            # TODO Handle exception
            raise e

    def _handle_received_error(self, frame: Frame) -> None:
        # TODO
        pass
