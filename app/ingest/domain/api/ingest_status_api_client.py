from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest_status import IngestStatus


class IIngestStatusApiClient(ABC):

    @abstractmethod
    def report_status(self, package_id: str, ingest_status: IngestStatus) -> None:
        pass
