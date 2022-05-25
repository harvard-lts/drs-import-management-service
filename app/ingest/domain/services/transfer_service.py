from logging import Logger

from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException
from app.ingest.domain.services.exceptions.transfer_status_message_handling_exception import \
    TransferStatusMessageHandlingException
from app.ingest.domain.services.ingest_service import IngestService


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

        :raises TransferStatusMessageHandlingException
        """
        try:
            package_id = message_body['package_id']
            self.__logger.info("Obtaining ingest by the package id of the received message {}...".format(package_id))
            ingest = self.__ingest_service.get_ingest_by_package_id(package_id)

            transfer_status = message_body['transfer_status']
            if transfer_status == "failure":
                self.__logger.info("Setting ingest as transferred failed...")
                self.__ingest_service.set_ingest_as_transferred_failed(ingest)
                return

            self.__logger.info("Setting ingest as transferred...")
            self.__ingest_service.set_ingest_as_transferred(ingest)

            self.__logger.info("Starting ingest processing...")
            self.__ingest_service.process_ingest(ingest)

        except (IngestServiceException, KeyError) as e:
            raise TransferStatusMessageHandlingException(message_id, str(e))
