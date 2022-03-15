from typing import Tuple, Dict

from app.containers import Services
from app.ingest.domain.services.ingest_service import IngestService


class IngestPostController:

    def __init__(self, ingest_service: IngestService = Services.ingest_service()) -> None:
        self.__ingest_service = ingest_service

    def __call__(self) -> Tuple[Dict, int]:
        # Fake behavior
        self.__ingest_service.initiate_ingest()
        return {"data": {"ingest_status": "processing_ingest"}}, 202
