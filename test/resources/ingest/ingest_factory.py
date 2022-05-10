from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


def create_ingest() -> Ingest:
    return Ingest(
        package_id="test_package_id",
        s3_path="test_s3_path",
        s3_bucket_name="test_s3_bucket_name",
        admin_metadata={
            "test_admin_metadata_field_1": "test",
            "test_admin_metadata_field_2": "test"
        },
        status=IngestStatus.pending_transfer_to_dropbox,
        depositing_application=DepositingApplication.Dataverse,
        drs_url=None
    )
