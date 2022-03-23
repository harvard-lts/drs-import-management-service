from app.ingest.domain.models.ingest.ingest import Ingest


def create_ingest() -> Ingest:
    return Ingest(
        package_id="test_package_id",
        s3_path="test_s3_path",
        s3_bucket_name="test_s3_bucket_name",
        dropbox_name="test_dropbox_name",
        admin_metadata={
            "test_admin_metadata_field_1": "test",
            "test_admin_metadata_field_2": "test"
        }
    )
