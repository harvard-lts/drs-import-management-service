from unittest import TestCase

from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException
from app.ingest.infrastructure.api.dataverse_ingest_status import DataverseIngestStatus


class TestDataverseParamsTransformer(TestCase):

    def setUp(self) -> None:
        self.sut = DataverseParamsTransformer()

    def test_transform_package_id_to_dataverse_params_happy_path(self) -> None:
        test_package_id = "doi-10-5072-fk2-e6cmkr.v1.18"
        actual_doi, actual_version = self.sut.transform_package_id_to_dataverse_params(test_package_id)

        expected_doi = "10.5072/FK2/E6CMKR"
        expected_version = "1.18"

        self.assertEqual(actual_doi, expected_doi)
        self.assertEqual(actual_version, expected_version)

    def test_transform_package_id_to_dataverse_params_malformed_short_package_id(self) -> None:
        test_package_id = "ab"
        with self.assertRaises(TransformPackageIdException):
            self.sut.transform_package_id_to_dataverse_params(test_package_id)

    def test_transform_package_id_to_dataverse_params_malformed_long_package_id(self) -> None:
        test_package_id = "doi-10-5072-fk2-e6cmkr1.18"
        with self.assertRaises(TransformPackageIdException):
            self.sut.transform_package_id_to_dataverse_params(test_package_id)

    def test_transform_ingest_status_to_dataverse_ingest_status_happy_path(self) -> None:
        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.batch_ingest_successful
        )
        expected_status = DataverseIngestStatus.success.value
        self.assertEqual(actual_status, expected_status)

        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.batch_ingest_failed
        )
        expected_status = DataverseIngestStatus.failure.value
        self.assertEqual(actual_status, expected_status)

        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.transferred_to_dropbox_failed
        )
        expected_status = DataverseIngestStatus.failure.value
        self.assertEqual(actual_status, expected_status)

        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.batch_ingest_failed
        )
        expected_status = DataverseIngestStatus.failure.value
        self.assertEqual(actual_status, expected_status)

        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.pending_transfer_to_dropbox
        )
        expected_status = DataverseIngestStatus.pending.value
        self.assertEqual(actual_status, expected_status)

        actual_status = self.sut.transform_ingest_status_to_dataverse_ingest_status(
            ingest_status=IngestStatus.processing_batch_ingest
        )
        expected_status = DataverseIngestStatus.pending.value
        self.assertEqual(actual_status, expected_status)
