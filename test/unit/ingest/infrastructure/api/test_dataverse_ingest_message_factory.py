from unittest import TestCase

from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_ingest_message_factory import DataverseIngestMessageFactory
from test.resources.ingest.ingest_factory import create_ingest


class TestDataverseIngestMessageFactory(TestCase):

    def setUp(self) -> None:
        self.sut = DataverseIngestMessageFactory()

    def test_get_dataverse_ingest_message_pending_transfer_to_dropbox_happy_path(self) -> None:
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.pending_transfer_to_dropbox)
        )
        expected_dataverse_ingest_message = "Pending transfer to Dropbox"
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)

    def test_get_dataverse_ingest_message_transferred_to_dropbox_successful_happy_path(self) -> None:
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.transferred_to_dropbox_successful)
        )
        expected_dataverse_ingest_message = "Successfully transferred to Dropbox"
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)

    def test_get_dataverse_ingest_message_transferred_to_dropbox_failed_happy_path(self) -> None:
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.transferred_to_dropbox_failed)
        )
        expected_dataverse_ingest_message = "Dropbox transfer failed"
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)

    def test_get_dataverse_ingest_message_processing_batch_ingest_happy_path(self) -> None:
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.processing_batch_ingest)
        )
        expected_dataverse_ingest_message = "Processing batch ingest"
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)

    def test_get_dataverse_ingest_message_batch_ingest_successful_happy_path(self) -> None:
        test_drs_url = "test_drs_url"
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.batch_ingest_successful, drs_url=test_drs_url)
        )
        expected_dataverse_ingest_message = test_drs_url
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)

    def test_get_dataverse_ingest_message_batch_ingest_failed_happy_path(self) -> None:
        actual_dataverse_ingest_message = self.sut.get_dataverse_ingest_message(
            create_ingest(status=IngestStatus.batch_ingest_failed)
        )
        expected_dataverse_ingest_message = "Batch ingest failed"
        self.assertEqual(actual_dataverse_ingest_message, expected_dataverse_ingest_message)
