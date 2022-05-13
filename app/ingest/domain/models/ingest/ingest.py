from dataclasses import dataclass
from typing import Optional

from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


@dataclass
class Ingest:
    package_id: str
    s3_path: str
    s3_bucket_name: str
    admin_metadata: dict
    status: IngestStatus
    depositing_application: DepositingApplication
    drs_url: Optional[str]
