from dependency_injector import containers, providers

from app.ingest.application.mq.initiate_ingest_queue_publisher import InitiateIngestQueuePublisher
from app.ingest.domain.services.ingest_service import IngestService


class Services(containers.DeclarativeContainer):
    ingest_service = providers.Factory(
        IngestService,
        initiate_ingest_queue_publisher=InitiateIngestQueuePublisher()
    )
