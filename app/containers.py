import logging

from dependency_injector import containers, providers

from app.common.application.controllers.responses.error_response_serializer import ErrorResponseSerializer
from app.health.application.controllers.services.git_service import GitService
from app.health.infrastructure.compound_connectivity_service import CompoundConnectivityService
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.services.process_service import ProcessService
from app.ingest.domain.services.transfer_service import TransferService
from app.ingest.infrastructure.api.dataverse_ingest_status_api_client import DataverseIngestStatusApiClient
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from app.ingest.infrastructure.data.repositories.ingest_repository import IngestRepository
from app.ingest.infrastructure.mq.publishers.process_ready_queue_publisher import ProcessReadyQueuePublisher
from app.ingest.infrastructure.mq.publishers.transfer_ready_queue_publisher import TransferReadyQueuePublisher


class Controllers(containers.DeclarativeContainer):
    error_response_serializer = providers.Factory(
        ErrorResponseSerializer
    )
    get_connectivity_service = providers.Factory(
        CompoundConnectivityService
    )
    git_service = providers.Factory(
        GitService
    )


class Services(containers.DeclarativeContainer):
    ingest_service = providers.Factory(
        IngestService,
        ingest_repository=IngestRepository(),
        transfer_ready_queue_publisher=TransferReadyQueuePublisher(),
        process_ready_queue_publisher=ProcessReadyQueuePublisher(),
        ingest_status_api_client=DataverseIngestStatusApiClient(
            dataverse_params_transformer=DataverseParamsTransformer()
        )
    )
    logger = logging.getLogger('dims')
    transfer_service = providers.Factory(
        TransferService,
        ingest_service=ingest_service,
        logger=logger
    )
    process_service = providers.Factory(
        ProcessService,
        ingest_service=ingest_service,
        logger=logger
    )
