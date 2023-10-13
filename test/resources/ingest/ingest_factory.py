from typing import Optional

from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


def create_ingest(
        package_id: str = "test_package_id",
        status: IngestStatus = IngestStatus.pending_transfer_to_dropbox,
        drs_url: Optional[str] = None
) -> Ingest:
    return Ingest(
        package_id=package_id,
        s3_path="test_s3_path",
        s3_bucket_name="test_s3_bucket_name",
        fs_source_path="test_fs_source_path",
        admin_metadata={
            "test_admin_metadata_field_1": "test",
            "test_admin_metadata_field_2": "test"
        },
        status=status,
        depositing_application="Dataverse",
        drs_url=drs_url
    )
