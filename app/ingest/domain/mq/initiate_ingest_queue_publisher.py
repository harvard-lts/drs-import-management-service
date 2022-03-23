"""
This module defines an IInitiateIngestQueuePublisher, which is a domain interface that
defines the necessary methods to implement by an ingestion initiation queue publisher.
"""

from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest import Ingest


class IInitiateIngestQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self, ingest: Ingest) -> None:
        """
        Given an ingest, publishes a message with the ingest details to MQ.

        :param ingest: Source ingest to compose and publish the message
        :type ingest: Ingest
        """
