from unittest import TestCase
from unittest.mock import Mock

from app.ingest.domain.mq.initiate_ingest_queue_publisher import IInitiateIngestQueuePublisher
from app.ingest.domain.mq.mq_connection_exception import MqConnectionException
from app.ingest.domain.mq.mq_message_publish_exception import MqMessagePublishException
from app.ingest.domain.services.ingest_service import IngestService


class TestIngestService(TestCase):

    def test_initiate_ingest_happy_path(self) -> None:
        initiate_ingest_queue_publisher_mock = Mock(spec=IInitiateIngestQueuePublisher)
        sut = IngestService(initiate_ingest_queue_publisher_mock)

        sut.initiate_ingest()

        initiate_ingest_queue_publisher_mock.publish_message.assert_called_once()

    def test_initiate_ingest_publisher_raises_mq_connection_exception(self) -> None:
        initiate_ingest_queue_publisher_stub = Mock(spec=IInitiateIngestQueuePublisher)
        initiate_ingest_queue_publisher_stub.publish_message.side_effect = MqConnectionException("test", "test", "test")
        sut = IngestService(initiate_ingest_queue_publisher_stub)

        with self.assertRaises(MqConnectionException):
            sut.initiate_ingest()

    def test_initiate_ingest_publisher_raises_mq_message_publish_exception(self) -> None:
        initiate_ingest_queue_publisher_stub = Mock(spec=IInitiateIngestQueuePublisher)
        initiate_ingest_queue_publisher_stub.publish_message.side_effect = MqMessagePublishException("test", "test",
                                                                                                     "test", "test")
        sut = IngestService(initiate_ingest_queue_publisher_stub)

        with self.assertRaises(MqMessagePublishException):
            sut.initiate_ingest()
