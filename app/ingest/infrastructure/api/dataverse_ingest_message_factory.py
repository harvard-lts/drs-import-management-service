from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


class DataverseIngestMessageFactory:
    __DATAVERSE_MESSAGE_PENDING_TRANSFER_TO_DROPBOX = "Pending transfer to Dropbox"
    __DATAVERSE_MESSAGE_TRANSFERED_TO_DROPBOX_SUCCESSFUL = "Successfully transferred to Dropbox"
    __DATAVERSE_MESSAGE_TRANSFERED_TO_DROPBOX_FAILED = "Dropbox transfer failed"
    __DATAVERSE_MESSAGE_PROCESSING_BATCH_INGEST = "Processing batch ingest"
    __DATAVERSE_MESSAGE_BATCH_INGEST_FAILED = "Batch ingest failed"

    def get_dataverse_ingest_message(self, ingest: Ingest) -> str:
        return {
            IngestStatus.pending_transfer_to_dropbox: self.__DATAVERSE_MESSAGE_PENDING_TRANSFER_TO_DROPBOX,
            IngestStatus.transferred_to_dropbox_successful: self.__DATAVERSE_MESSAGE_TRANSFERED_TO_DROPBOX_SUCCESSFUL,
            IngestStatus.transferred_to_dropbox_failed: self.__DATAVERSE_MESSAGE_TRANSFERED_TO_DROPBOX_FAILED,
            IngestStatus.processing_batch_ingest: self.__DATAVERSE_MESSAGE_PROCESSING_BATCH_INGEST,
            IngestStatus.batch_ingest_successful: ingest.drs_url,
            IngestStatus.batch_ingest_failed: self.__DATAVERSE_MESSAGE_BATCH_INGEST_FAILED,
        }.get(ingest.status, "")
