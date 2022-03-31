from enum import auto

from app.common.domain.auto_name_enum import AutoNameEnum


class IngestStatus(AutoNameEnum):
    pending_transfer_to_dropbox = auto()
    transferred_to_dropbox_successful = auto()
    transferred_to_dropbox_failed = auto()
    processing_batch_ingest = auto()
    batch_ingest_successful = auto()
    batch_ingest_failed = auto()
