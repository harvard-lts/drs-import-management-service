"""
This module defines an IProcessReadyQueuePublisher, which is a domain interface that
defines the necessary methods to implement by a process ready queue publisher.
"""

from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest import Ingest


class IProcessReadyQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self, ingest: Ingest) -> None:
        """
        Given an ingest, publishes a process ready message with the ingest details to MQ.

        :param ingest: Source ingest to compose and publish the process ready message
        :type ingest: Ingest

        :raises MqException
        """
