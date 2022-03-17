"""
This module defines an IInitiateIngestQueuePublisher, which is a domain interface that
defines the necessary methods to implement by an ingestion initiation queue publisher.
"""

from abc import ABC, abstractmethod


class IInitiateIngestQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self) -> None:
        """
        Publishes a message with ingest details to MQ.
        """
