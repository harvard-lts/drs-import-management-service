from dependency_injector import containers, providers

from app.ingest.application.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from app.ingest.domain.services.ingest_service import IngestService


class Services(containers.DeclarativeContainer):
    ingest_service = providers.Factory(
        IngestService,
        transfer_ready_queue_publisher=TransferReadyQueuePublisher()
    )
