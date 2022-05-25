"""
This module defines a ProcessService, which is a domain service that defines Process operations.
"""

from logging import Logger

from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException
from app.ingest.domain.services.exceptions.process_status_message_handling_exception import \
    ProcessStatusMessageHandlingException
from app.ingest.domain.services.exceptions.process_status_message_missing_field_exception import \
    ProcessStatusMessageMissingFieldException
from app.ingest.domain.services.ingest_service import IngestService


class ProcessService:
    def __init__(
            self,
            ingest_service: IngestService,
            logger: Logger
    ) -> None:
        self.__ingest_service = ingest_service
        self.__logger = logger

    def handle_process_status_message(self, message_body: dict, message_id: str) -> None:
        """
        Handles a Process Status message.

        :param message_body: message body
        :type message_body: dict
        :param message_id: message id
        :type message_id: str

        :raises ProcessServiceException
        """
        try:
            package_id = message_body['package_id']
            process_status = message_body['batch_ingest_status']
            drs_url = message_body['drs_url']
        except KeyError as e:
            raise ProcessStatusMessageMissingFieldException(message_id, str(e))

        self.__logger.info("Obtaining ingest by the package id of the received message " + package_id + "...")
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)

            if process_status == "failure":
                self.__logger.info("Setting ingest as processed failed...")
                self.__ingest_service.set_ingest_as_processed_failed(ingest)
                return

            self.__logger.info("Setting ingest as processed...")
            self.__ingest_service.set_ingest_as_processed(ingest, drs_url)

        except IngestServiceException as e:
            raise ProcessStatusMessageHandlingException(message_id, str(e))
