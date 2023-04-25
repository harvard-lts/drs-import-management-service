"""
This module defines a TransferService, which is a domain service that defines Transfer operations.
"""

from logging import Logger

from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException
from app.ingest.domain.services.exceptions.message_body_field_exception import MessageBodyFieldException
from app.ingest.domain.services.exceptions.transfer_status_message_handling_exception import \
    TransferStatusMessageHandlingException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.services.message_body_transformer import MessageBodyTransformer


class TransferService:
    def __init__(
            self,
            ingest_service: IngestService,
            logger: Logger
    ) -> None:
        self.__ingest_service = ingest_service
        self.__logger = logger

    def handle_transfer_status_message(self, message_body: dict, message_id: str) -> None:
        """
        Handles a Transfer Status message.

        :param message_body: message body
        :type message_body: dict
        :param message_id: message id
        :type message_id: str

        :raises TransferServiceException
        """
        message_body_transformer = MessageBodyTransformer()
        try:
            package_id = message_body_transformer.get_message_body_field_value(
                'package_id',
                message_body,
                message_id
            )
            transfer_status = message_body_transformer.get_message_body_field_value(
                'transfer_status',
                message_body,
                message_id
            )
        except MessageBodyFieldException as e:
            raise TransferStatusMessageHandlingException(message_id, str(e)) from e

        self.__logger.info("Obtaining ingest by the package id of the received message {}...".format(package_id))
        try:
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)

            if transfer_status == "failure":
                self.__logger.info("Setting ingest as transferred failed...")
                self.__ingest_service.set_ingest_as_transferred_failed(ingest)
                return

            self.__logger.info("Setting ingest as transferred...")
            self.__ingest_service.set_ingest_as_transferred(ingest)

            self.__logger.info("Starting ingest processing...")
            self.__ingest_service.process_ingest(ingest)

        except IngestServiceException as e:
            raise TransferStatusMessageHandlingException(message_id, str(e)) from e
