"""
This module defines an IngestService, which is a domain service that defines ingesting operations.
"""

from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.exceptions.mq_exception import MqException
from app.ingest.domain.mq.transfer_ready_queue_publisher import ITransferReadyQueuePublisher
from app.ingest.domain.services.exceptions.initiate_ingest_exception import InitiateIngestException


class IngestService:

    def __init__(self, transfer_ready_queue_publisher: ITransferReadyQueuePublisher) -> None:
        """
        :param transfer_ready_queue_publisher: an implementation of ITransferReadyQueuePublisher
        :type transfer_ready_queue_publisher: ITransferReadyQueuePublisher
        """
        self.__transfer_ready_queue_publisher = transfer_ready_queue_publisher

    def initiate_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest by calling transfer ready queue publisher to publish a message.

        :param ingest: Ingest to initiate
        :type ingest: Ingest
        """
        try:
            self.__transfer_ready_queue_publisher.publish_message(ingest)
        except MqException as mqe:
            raise InitiateIngestException(str(mqe))
