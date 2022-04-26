"""
This module defines an IngestService, which is a domain service that defines ingesting operations.
"""

from app.ingest.domain.api.exceptions.report_status_api_client_exception import ReportStatusApiClientException
from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.mq.exceptions.mq_exception import MqException
from app.ingest.domain.mq.process_ready_queue_publisher import IProcessReadyQueuePublisher
from app.ingest.domain.mq.transfer_ready_queue_publisher import ITransferReadyQueuePublisher
from app.ingest.domain.repositories.exceptions.ingest_query_exception import IngestQueryException
from app.ingest.domain.repositories.exceptions.ingest_save_exception import IngestSaveException
from app.ingest.domain.repositories.ingest_repository import IIngestRepository
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_failed_exception import \
    SetIngestAsTransferredFailedException
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException


class IngestService:

    def __init__(
            self,
            ingest_repository: IIngestRepository,
            transfer_ready_queue_publisher: ITransferReadyQueuePublisher,
            process_ready_queue_publisher: IProcessReadyQueuePublisher,
            ingest_status_api_client: IIngestStatusApiClient
    ) -> None:
        """
        :param ingest_repository: an implementation of IIngestRepository
        :type ingest_repository: IIngestRepository
        :param transfer_ready_queue_publisher: an implementation of ITransferReadyQueuePublisher
        :type transfer_ready_queue_publisher: ITransferReadyQueuePublisher
        :param process_ready_queue_publisher: an implementation of IProcessReadyQueuePublisher
        :type process_ready_queue_publisher: IProcessReadyQueuePublisher
        :param ingest_status_api_client: an implementation of IIngestStatusApiClient
        :type ingest_status_api_client: IIngestStatusApiClient
        """
        self.__ingest_repository = ingest_repository
        self.__transfer_ready_queue_publisher = transfer_ready_queue_publisher
        self.__process_ready_queue_publisher = process_ready_queue_publisher
        self.__ingest_status_api_client = ingest_status_api_client

    def get_ingest_by_package_id(self, ingest_package_id: str) -> Ingest:
        """
        Retrieves an ingest by calling the ingest repository.

        :param ingest_package_id: Ingest package id
        :type ingest_package_id: str

        :raises GetIngestByPackageIdException
        """
        try:
            ingest = self.__ingest_repository.get_by_package_id(ingest_package_id)
            if ingest is None:
                raise GetIngestByPackageIdException(ingest_package_id,
                                                    f"No ingest found for package id {ingest_package_id}")
            return ingest
        except IngestQueryException as iqe:
            raise GetIngestByPackageIdException(ingest_package_id, str(iqe))

    def transfer_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest transfer by calling transfer ready queue publisher and by updating
        its status.

        :param ingest: Ingest to transfer
        :type ingest: Ingest

        :raises TransferIngestException
        """
        try:
            self.__transfer_ready_queue_publisher.publish_message(ingest)
            ingest.status = IngestStatus.pending_transfer_to_dropbox
            self.__ingest_repository.save(ingest)
        except (MqException, IngestSaveException) as e:
            raise TransferIngestException(ingest.package_id, str(e))

    def set_ingest_as_transferred(self, ingest: Ingest, ingest_destination_path: str) -> None:
        """
        Sets an ingest as transferred by updating its status and by setting its destination path.

        :param ingest: Ingest to set as transferred
        :type ingest: Ingest
        :param ingest_destination_path: Ingest destination path
        :type ingest_destination_path: str

        :raises SetIngestAsTransferredException
        """
        ingest.status = IngestStatus.transferred_to_dropbox_successful
        ingest.destination_path = ingest_destination_path
        try:
            self.__ingest_repository.save(ingest)
        except IngestSaveException as ise:
            raise SetIngestAsTransferredException(ingest.package_id, str(ise))

    def set_ingest_as_transferred_failed(self, ingest: Ingest) -> None:
        """
        Sets an ingest as transferred failed by reporting and updating its status.

        :param ingest: Ingest to report and update as transferred failed
        :type ingest: Ingest

        :raises SetIngestAsTransferredFailedException
        """
        ingest.status = IngestStatus.transferred_to_dropbox_failed
        try:
            self.__ingest_status_api_client.report_status(ingest.package_id, ingest.status)
            self.__ingest_repository.save(ingest)
        except (ReportStatusApiClientException, IngestSaveException) as e:
            raise SetIngestAsTransferredFailedException(ingest.package_id, str(e))

    def process_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest process by calling process ready queue publisher and by updating
        its status.

        :param ingest: Ingest to process
        :type ingest: Ingest

        :raises ProcessIngestException
        """
        ingest.status = IngestStatus.processing_batch_ingest
        try:
            self.__process_ready_queue_publisher.publish_message(ingest)
            self.__ingest_repository.save(ingest)
        except (MqException, IngestSaveException) as e:
            raise ProcessIngestException(ingest.package_id, str(e))

    def set_ingest_as_processed(self, ingest: Ingest) -> None:
        """
        Sets an ingest as processed by reporting and updating its status.

        :param ingest: Ingest to report and update as processed
        :type ingest: Ingest

        :raises SetIngestAsProcessedException
        """
        ingest.status = IngestStatus.batch_ingest_successful
        try:
            self.__ingest_status_api_client.report_status(ingest.package_id, ingest.status)
            self.__ingest_repository.save(ingest)
        except (ReportStatusApiClientException, IngestSaveException) as e:
            raise SetIngestAsProcessedException(ingest.package_id, str(e))
