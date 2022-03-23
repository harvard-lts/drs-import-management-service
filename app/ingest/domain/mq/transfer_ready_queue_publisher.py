"""
This module defines an ITransferReadyQueuePublisher, which is a domain interface that
defines the necessary methods to implement by a transfer ready queue publisher.
"""

from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest import Ingest


class ITransferReadyQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self, ingest: Ingest) -> None:
        """
        Given an ingest, publishes a transfer ready message with the ingest details to MQ.

        :param ingest: Source ingest to compose and publish the transfer ready message
        :type ingest: Ingest
        """
