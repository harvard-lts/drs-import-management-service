"""
This module defines an IProcessReadyQueuePublisher, which is a domain interface that
defines the necessary methods to implement by a process ready queue publisher.
"""

from abc import ABC, abstractmethod


class IProcessReadyQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self) -> None:
        """
        Publishes a process ready message to MQ.
        """
