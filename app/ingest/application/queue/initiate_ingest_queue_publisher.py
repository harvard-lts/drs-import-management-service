from app.ingest.domain.queue.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher


class InitiateIngestQueuePublisher(IInitiateIngestQueuePublisher):

    def publish_message(self) -> None:
        pass
