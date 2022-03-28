from typing import Tuple, Dict

from app.containers import Services
from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException
from app.ingest.domain.services.ingest_service import IngestService


class IngestPostController:

    def __init__(self, ingest_service: IngestService = Services.ingest_service()) -> None:
        self.__ingest_service = ingest_service

    def __call__(self) -> Tuple[Dict, int]:
        try:
            self.__ingest_service.transfer_ingest(
                # TODO: Fake ingest until advanced controller is implemented
                # https://github.com/harvard-lts/HDC/issues/105
                Ingest(
                    package_id="",
                    s3_path="",
                    s3_bucket_name="",
                    dropbox_name="",
                    destination_path=None,
                    admin_metadata={},
                    # TODO: Initial ingest status
                    status=IngestStatus.pending_transfer_to_dropbox,
                    depositing_application=DepositingApplication.Dataverse
                )
            )
        except TransferIngestException as tie:
            return {"data": None, "error": str(tie)}, 500

        return {"data": {"ingest_status": "processing_ingest"}, "error": None}, 202
