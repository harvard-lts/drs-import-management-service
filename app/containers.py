import os

from dependency_injector import containers, providers

from app.common.application.controllers.jwt_decoder import JwtDecoder
from app.common.application.controllers.responses.error.error_response_serializer import ErrorResponseSerializer
from app.ingest.application.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from app.ingest.application.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher
from app.ingest.data.repositories.ingest_repository import IngestRepository
from app.ingest.domain.services.ingest_service import IngestService


class Controllers(containers.DeclarativeContainer):
    jwt_decoder = providers.Factory(
        JwtDecoder,
        public_jwt_key=os.getenv('PUBLIC_JWT_KEY')
    )
    error_response_serializer = providers.Factory(
        ErrorResponseSerializer
    )


class Services(containers.DeclarativeContainer):
    ingest_service = providers.Factory(
        IngestService,
        ingest_repository=IngestRepository(),
        transfer_ready_queue_publisher=TransferReadyQueuePublisher(),
        process_ready_queue_publisher=ProcessReadyQueuePublisher()
    )
