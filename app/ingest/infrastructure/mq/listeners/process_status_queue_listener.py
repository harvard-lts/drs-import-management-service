"""
This module defines an ProcessStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for process status messages.
"""
import os

from app.common.infrastructure.mq.listeners.stomp_listener_base import StompListenerBase
from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.containers import Services
from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException
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

    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        self._logger.info(
            "Received message from Process Queue. Message body: {}. Message id: {}".format(
                str(message_body),
                message_id
            )
        )
        try:
            package_id = message_body['package_id']
            self._logger.info("Obtaining ingest by the package id of the received message " + package_id + "...")
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)

            transfer_status = message_body['batch_ingest_status']
            if transfer_status == "failure":
                self._logger.info("Setting ingest as processed failed...")
                self.__ingest_service.set_ingest_as_processed_failed(ingest)
                self._acknowledge_message(message_id, message_subscription)
                return

            self._logger.info("Setting ingest as processed...")
            self.__ingest_service.set_ingest_as_processed(ingest, message_body["drs_url"])

            self._acknowledge_message(message_id, message_subscription)

        except (IngestServiceException, KeyError) as e:
            self._logger.error(str(e))
            self._unacknowledge_message(message_id, message_subscription)
