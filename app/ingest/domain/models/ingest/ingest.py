from dataclasses import dataclass


@dataclass
class Ingest:
    package_id: str
    s3_path: str
    s3_bucket_name: str
    dropbox_name: str
    admin_metadata: dict
