"""
This module defines a TransferStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for transfer status messages.
"""
import json
import os

from stomp.utils import Frame

from app.containers import Services
from app.ingest.application.mq.listeners.stomp_listener_base import StompListenerBase
from app.ingest.application.mq.mq_connection_params import MqConnectionParams
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

    def _handle_received_message(self, frame: Frame) -> None:
        # TODO Handle transfer_status: Currently only considered successful

        try:
            message_body = json.loads(frame.body)
        except json.decoder.JSONDecodeError as e:
            # TODO Handle exception
            raise e

        # TODO: Fake ingest until MongoDB persistence is implemented
        # https://github.com/harvard-lts/HDC/issues/104
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(message_body['package_id'])
        except GetIngestByPackageIdException as e:
            # TODO Handle exception
            raise e

        try:
            self.__ingest_service.set_ingest_as_transferred(ingest, message_body['destination_path'])
        except SetIngestAsTransferredException as e:
            # TODO Handle exception
            raise e

        try:
            self.__ingest_service.process_ingest(ingest)
        except ProcessIngestException as e:
            # TODO Handle exception
            raise e

    def _handle_received_error(self, frame: Frame) -> None:
        # TODO Handle error
        pass
