from typing import Optional

from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.repositories.ingest_repository import IIngestRepository


# TODO: MongoDB implementation logic
class IngestRepository(IIngestRepository):

    def get_by_package_id(self, package_id: str) -> Optional[Ingest]:
        pass

    def save(self, ingest: Ingest) -> None:
        pass
