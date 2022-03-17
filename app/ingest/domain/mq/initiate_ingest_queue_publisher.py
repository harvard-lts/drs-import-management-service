from abc import ABC, abstractmethod


class IInitiateIngestQueuePublisher(ABC):

    @abstractmethod
    def publish_message(self) -> None:
        """
        Publish a message with ingest details to MQ.
        """
