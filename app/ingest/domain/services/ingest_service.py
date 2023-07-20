"""
This module defines an IngestService, which is a domain service that defines ingesting operations.
"""

from app.ingest.domain.api.exceptions.report_status_api_client_exception import ReportStatusApiClientException
from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.repositories.exceptions.ingest_query_exception import IngestQueryException
from app.ingest.domain.repositories.exceptions.ingest_save_exception import IngestSaveException
from app.ingest.domain.repositories.ingest_repository import IIngestRepository
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_failed_exception import \
    SetIngestAsProcessedFailedException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_failed_exception import \
    SetIngestAsTransferredFailedException
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException
from kombu.exceptions import OperationalError
from celery import Celery
import os
import os.path

app = Celery('tasks')
app.config_from_object('celeryconfig')

process_ready_task = os.getenv('PROCESS_READY_TASK_NAME', 'dts.tasks.prepare_and_send_to_drs')
transfer_ready_task = os.getenv('TRANSFER_READY_TASK_NAME', 'transfer_service.tasks.transfer_data')

class IngestService:

    def __init__(
            self,
            ingest_repository: IIngestRepository,
            ingest_status_api_client: IIngestStatusApiClient
    ) -> None:
        """
        :param ingest_repository: an implementation of IIngestRepository
        :type ingest_repository: IIngestRepository
        :param ingest_status_api_client: an implementation of IIngestStatusApiClient
        :type ingest_status_api_client: IIngestStatusApiClient
        """
        self.__ingest_repository = ingest_repository
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
            raise GetIngestByPackageIdException(ingest_package_id, str(iqe)) from iqe

    def transfer_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest transfer by calling transfer_data task and by updating
        its status.

        :param ingest: Ingest to transfer
        :type ingest: Ingest

        :raises TransferIngestException
        """
        ingest.status = IngestStatus.pending_transfer_to_dropbox
        msg_json = self.__create_transfer_ready_message(ingest)
        try:
            app.send_task(transfer_ready_task, args=[msg_json], kwargs={},
                    queue=os.getenv("TRANSFER_PUBLISH_QUEUE_NAME")) 
    
            self.__ingest_repository.save(ingest)
        except (IngestSaveException) as e:
            raise TransferIngestException(ingest.package_id, str(e)) from e

    def set_ingest_as_transferred(self, ingest: Ingest) -> None:
        """
        Sets an ingest as transferred by updating and reporting its status.

        :param ingest: Ingest to set as transferred
        :type ingest: Ingest

        :raises SetIngestAsTransferredException
        """
        ingest.status = IngestStatus.transferred_to_dropbox_successful
        try:
            self.__ingest_repository.save(ingest)
            if ingest.depositing_application == "Dataverse":
                self.__ingest_status_api_client.report_status(ingest)
        except (IngestSaveException, ReportStatusApiClientException) as e:
            raise SetIngestAsTransferredException(ingest.package_id, str(e)) from e

    def set_ingest_as_transferred_failed(self, ingest: Ingest) -> None:
        """
        Sets an ingest as transferred failed by updating and reporting its status.

        :param ingest: Ingest to report and update as transferred failed
        :type ingest: Ingest

        :raises SetIngestAsTransferredFailedException
        """
        ingest.status = IngestStatus.transferred_to_dropbox_failed
        try:
            self.__ingest_repository.save(ingest)
            if ingest.depositing_application == "Dataverse":
                self.__ingest_status_api_client.report_status(ingest)
        except (IngestSaveException, ReportStatusApiClientException) as e:
            raise SetIngestAsTransferredFailedException(ingest.package_id, str(e)) from e

    def process_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest process by calling prepare_and_send_to_drs task and by updating
        and reporting its status.

        :param ingest: Ingest to process
        :type ingest: Ingest

        :raises ProcessIngestException
        """
        ingest.status = IngestStatus.processing_batch_ingest
        msg_json = self.__create_process_ready_message(ingest)
        try:
            app.send_task(process_ready_task, args=[msg_json], kwargs={},
                    queue=os.getenv("PROCESS_PUBLISH_QUEUE_NAME")) 
            self.__ingest_repository.save(ingest)
            if ingest.depositing_application == "Dataverse":
                self.__ingest_status_api_client.report_status(ingest)
        except (OperationalError, IngestSaveException, ReportStatusApiClientException) as e:
            raise ProcessIngestException(ingest.package_id, str(e)) from e

    def set_ingest_as_processed(self, ingest: Ingest, drs_url: str) -> None:
        """
        Sets an ingest as processed by updating its DRS URL and by updating and reporting its status.

        :param ingest: Ingest to report and update as processed
        :type ingest: Ingest
        :param drs_url: DRS URL of the processed object
        :type drs_url: str

        :raises SetIngestAsProcessedException
        """
        ingest.status = IngestStatus.batch_ingest_successful
        ingest.drs_url = drs_url
        try:
            self.__ingest_repository.save(ingest)
            if ingest.depositing_application == "Dataverse":
                self.__ingest_status_api_client.report_status(ingest)
        except (IngestSaveException, ReportStatusApiClientException) as e:
            raise SetIngestAsProcessedException(ingest.package_id, str(e)) from e

    def set_ingest_as_processed_failed(self, ingest: Ingest) -> None:
        """
        Sets an ingest as processed failed by updating and reporting its status.

        :param ingest: Ingest to report and update as processed failed
        :type ingest: Ingest

        :raises SetIngestAsProcessedFailedException
        """
        ingest.status = IngestStatus.batch_ingest_failed
        try:
            self.__ingest_repository.save(ingest)
            if ingest.depositing_application == "Dataverse":
                self.__ingest_status_api_client.report_status(ingest)
        except (IngestSaveException, ReportStatusApiClientException) as e:
            raise SetIngestAsProcessedFailedException(ingest.package_id, str(e)) from e
        
    def __create_transfer_ready_message(self, ingest: Ingest) -> dict:
        # Set destination path based on application
        base_dropbox_path = os.getenv('BASE_DROPBOX_PATH', '/drs2dev/drsfs/dropboxes/')
        destination_path = ""

        if ingest.depositing_application == "Dataverse":
            destination_path = os.path.join(base_dropbox_path, os.getenv('DATAVERSE_DROPBOX_NAME', 'dvndev'), "incoming")
        elif ingest.depositing_application == "ePADD":
            destination_path = os.path.join(base_dropbox_path, os.getenv('EPADD_DROPBOX_NAME', 'epadddev_secure'), "incoming")

        ingest.admin_metadata["task_name"] = transfer_ready_task
        return {
            'package_id': ingest.package_id,
            's3_path': ingest.s3_path,
            's3_bucket_name': ingest.s3_bucket_name,
            'destination_path': destination_path,
            'application_name': ingest.depositing_application,
            'admin_metadata': ingest.admin_metadata
        }
        
    def __create_process_ready_message(self, ingest: Ingest) -> dict:
        # Set destination path based on application
        base_dropbox_path = os.getenv('BASE_DROPBOX_PATH', '/drs2dev/drsfs/dropboxes/')
        destination_path = ""

        if ingest.depositing_application == "Dataverse":
            destination_path = os.path.join(base_dropbox_path, os.getenv('DATAVERSE_DROPBOX_NAME', 'dvndev'), "incoming")
        elif ingest.depositing_application == "ePADD":
            destination_path = os.path.join(base_dropbox_path, os.getenv('EPADD_DROPBOX_NAME', 'epadddev-secure'), "incoming")

        ingest.admin_metadata["task_name"] = process_ready_task
        if ingest.dry_run is None:
            return {
                'package_id': ingest.package_id,
                'destination_path': destination_path,
                'admin_metadata': ingest.admin_metadata,
                'application_name': ingest.depositing_application
            }
        else:
            return {
                'package_id': ingest.package_id,
                'destination_path': destination_path,
                'admin_metadata': ingest.admin_metadata,
                'application_name': ingest.depositing_application,
                'dry_run': ingest.dry_run
            }
