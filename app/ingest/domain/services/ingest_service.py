"""
This module defines an IngestService, which is a domain service that defines ingesting operations
"""

from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.exceptions.mq_exception import MqException
from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher
from app.ingest.domain.services.exceptions.initiate_ingest_exception import InitiateIngestException


class IngestService:

    def __init__(self, initiate_ingest_queue_publisher: IInitiateIngestQueuePublisher) -> None:
        """
        :param initiate_ingest_queue_publisher: an implementation of IInitiateIngestQueuePublisher
        :type initiate_ingest_queue_publisher: IInitiateIngestQueuePublisher
        """
        self.__initiate_ingest_queue_publisher = initiate_ingest_queue_publisher

    def initiate_ingest(self, ingest: Ingest) -> None:
        """
        Initiates an ingest by calling ingest queue publisher to publish an ingest message.

        :param ingest: Ingest to initiate
        :type ingest: Ingest
        """
        try:
            self.__initiate_ingest_queue_publisher.publish_message(ingest)
        except MqException as mqe:
            raise InitiateIngestException(str(mqe))
