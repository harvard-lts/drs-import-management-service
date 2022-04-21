from typing import Optional

from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.repositories.ingest_repository import IIngestRepository


# TODO: MongoDB implementation logic
class IngestRepository(IIngestRepository):

    def get_by_package_id(self, package_id: str) -> Optional[Ingest]:
        # TODO: Fake ingest until MongoDB persistence is implemented
        # https://github.com/harvard-lts/HDC/issues/104
        return Ingest(
            package_id=package_id,
            s3_path="dummy_s3_path",
            s3_bucket_name="dummy_s3_bucket_name",
            admin_metadata={},
            status=IngestStatus.pending_transfer_to_dropbox,
            depositing_application=DepositingApplication.Dataverse
        )

    def save(self, ingest: Ingest) -> None:
        pass
