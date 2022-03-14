from unittest import TestCase
from unittest.mock import Mock

from app.ingest.domain.queue.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher
from app.ingest.domain.services.ingest_service import IngestService


class TestIngestService(TestCase):

    def test_initiate_ingest_happy_path(self):
        initiate_ingest_queue_publisher_mock = Mock(spec=IInitiateIngestQueuePublisher)
        sut = IngestService(initiate_ingest_queue_publisher_mock)

        sut.initiate_ingest()

        initiate_ingest_queue_publisher_mock.publish_message.assert_called_once()
