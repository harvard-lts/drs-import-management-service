"""
This module defines a ProcessService, which is a domain service that defines Process operations.
"""

from logging import Logger

from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException
from app.ingest.domain.services.exceptions.message_body_field_exception import MessageBodyFieldException
from app.ingest.domain.services.exceptions.process_status_message_handling_exception import \
    ProcessStatusMessageHandlingException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.services.message_body_transformer import MessageBodyTransformer


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
        message_body_transformer = MessageBodyTransformer()
        try:
            package_id = message_body_transformer.get_message_body_field_value(
                'package_id',
                message_body,
                message_id
            )
            process_status = message_body_transformer.get_message_body_field_value(
                'batch_ingest_status',
                message_body,
                message_id
            )
            depositing_application = message_body_transformer.get_message_body_field_value(
                'application_name',
                message_body,
                message_id
            )

            self.__logger.info("Obtaining ingest by the package id of the received message " + package_id + "...")
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)

            if depositing_application == "ePADD":
                return
            elif depositing_application == "Dataverse":
                if process_status == "failure":
                    self.__logger.info("Setting ingest as processed failed...")
                    self.__ingest_service.set_ingest_as_processed_failed(ingest)
                    return

                self.__logger.info("Setting ingest as processed...")
                drs_url = message_body_transformer.get_message_body_field_value('drs_url', message_body, message_id)
                self.__ingest_service.set_ingest_as_processed(ingest, drs_url)

        except (MessageBodyFieldException, IngestServiceException) as e:
            raise ProcessStatusMessageHandlingException(message_id, str(e))
