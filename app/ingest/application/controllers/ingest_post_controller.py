from typing import Tuple, Dict

from app.ingest.application.queue.initiate_ingest_queue_publisher import InitiateIngestQueuePublisher
from app.ingest.domain.services.ingest_service import IngestService


class IngestPostController:

    def __init__(self, ingest_service: IngestService) -> None:
        # TODO: Dependency Injection
        if ingest_service is None:
            self.__ingest_service = IngestService(InitiateIngestQueuePublisher())
        else:
            self.__ingest_service = ingest_service

    def __call__(self) -> Tuple[Dict, int]:
        # Fake behavior
        self.__ingest_service.initiate_ingest()
        return {"data": {"ingest_status": "processing_ingest"}}, 202
