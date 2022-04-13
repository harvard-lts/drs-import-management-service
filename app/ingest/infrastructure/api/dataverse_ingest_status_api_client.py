from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


class DataverseIngestStatusApiClient(IIngestStatusApiClient):

    def report_status(self, package_id: str, ingest_status: IngestStatus) -> None:
        pass
