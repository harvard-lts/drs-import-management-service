from app.ingest.application.mq.initiate_ingest_queue_publisher import InitiateIngestQueuePublisher
from test.integration.ingest.integration_test_base import IntegrationTestBase


class TestInitiateIngestQueuePublisher(IntegrationTestBase):

    def test_publish_message_happy_path(self) -> None:
        sut = InitiateIngestQueuePublisher()
        sut.publish_message()
