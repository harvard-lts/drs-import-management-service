from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher


class IngestService:

    def __init__(self, initiate_ingest_queue_publisher: IInitiateIngestQueuePublisher) -> None:
        self.__initiate_ingest_queue_publisher = initiate_ingest_queue_publisher

    def initiate_ingest(self) -> None:
        self.__initiate_ingest_queue_publisher.publish_message()
