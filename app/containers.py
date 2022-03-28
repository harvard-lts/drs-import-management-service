from dependency_injector import containers, providers

from app.ingest.application.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from app.ingest.application.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from app.ingest.data.repositories.ingest_repository import IngestRepository
from app.ingest.domain.services.ingest_service import IngestService


class Services(containers.DeclarativeContainer):
    ingest_service = providers.Factory(
        IngestService,
        ingest_repository=IngestRepository(),
        transfer_ready_queue_publisher=TransferReadyQueuePublisher(),
        process_ready_queue_publisher=ProcessReadyQueuePublisher()
    )
