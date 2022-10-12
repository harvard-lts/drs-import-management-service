from dataclasses import dataclass, field
from typing import Optional

from app.ingest.domain.models.ingest.ingest_status import IngestStatus


@dataclass
class Ingest:
    package_id: str
    s3_path: str
    s3_bucket_name: str
    admin_metadata: dict
    status: IngestStatus
    depositing_application: str
    drs_url: Optional[str]
    dry_run: Optional[str] = field(default=None)
