from typing import Tuple, Dict

from app.containers import Services
from app.ingest.domain.services.exceptions.initiate_ingest_exception import InitiateIngestException
from app.ingest.domain.services.ingest_service import IngestService


class IngestPostController:

    def __init__(self, ingest_service: IngestService = Services.ingest_service()) -> None:
        self.__ingest_service = ingest_service

    def __call__(self) -> Tuple[Dict, int]:
        try:
            self.__ingest_service.initiate_ingest()
        except InitiateIngestException as e:
            return {"data": None, "error": str(e)}, 500

        return {"data": {"ingest_status": "processing_ingest"}, "error": None}, 202
