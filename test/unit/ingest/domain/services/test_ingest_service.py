from dataclasses import replace
from unittest import TestCase
from unittest.mock import Mock

from app.ingest.domain.api.exceptions.report_status_api_client_exception import ReportStatusApiClientException
from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.repositories.exceptions.ingest_query_exception import IngestQueryException
from app.ingest.domain.repositories.exceptions.ingest_save_exception import IngestSaveException
from app.ingest.domain.repositories.ingest_repository import IIngestRepository
from app.ingest.domain.services.exceptions.get_ingest_by_package_id_exception import GetIngestByPackageIdException
from app.ingest.domain.services.exceptions.process_ingest_exception import ProcessIngestException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_exception import SetIngestAsProcessedException
from app.ingest.domain.services.exceptions.set_ingest_as_processed_failed_exception import \
    SetIngestAsProcessedFailedException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_exception import SetIngestAsTransferredException
from app.ingest.domain.services.exceptions.set_ingest_as_transferred_failed_exception import \
    SetIngestAsTransferredFailedException
from app.ingest.domain.services.ingest_service import IngestService
from test.resources.ingest.ingest_factory import create_ingest


class TestIngestService(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()

    def test_get_ingest_by_package_id_happy_path(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=Mock(spec=IIngestStatusApiClient)
        )

        test_package_id = self.TEST_INGEST.package_id
        sut.get_ingest_by_package_id(test_package_id)

        ingest_repository_mock.get_by_package_id.assert_called_once_with(test_package_id)

    def test_get_ingest_by_package_id_repository_returns_none(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.get_by_package_id.return_value = None

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=Mock(spec=IIngestStatusApiClient)
        )

        with self.assertRaises(GetIngestByPackageIdException):
            sut.get_ingest_by_package_id(self.TEST_INGEST.package_id)

    def test_get_ingest_by_package_id_repository_raises_ingest_query_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.get_by_package_id.side_effect = IngestQueryException("test", "test")

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=Mock(spec=IIngestStatusApiClient)
        )

        with self.assertRaises(GetIngestByPackageIdException):
            sut.get_ingest_by_package_id(self.TEST_INGEST.package_id)


    def test_set_ingest_as_transferred_happy_path(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        sut.set_ingest_as_transferred(self.TEST_INGEST)

        expected_ingest_parameter = replace(self.TEST_INGEST, status=IngestStatus.transferred_to_dropbox_successful)
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)
        ingest_status_api_client_mock.report_status.assert_called_once_with(expected_ingest_parameter)

    def test_set_ingest_as_transferred_repository_raises_ingest_save_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.save.side_effect = IngestSaveException("test", "test")
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        with self.assertRaises(SetIngestAsTransferredException):
            sut.set_ingest_as_transferred(self.TEST_INGEST)

        ingest_status_api_client_mock.report_status.assert_not_called()

    def test_set_ingest_as_transferred_failed_happy_path(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        sut.set_ingest_as_transferred_failed(self.TEST_INGEST)

        expected_ingest_parameter = replace(self.TEST_INGEST, status=IngestStatus.transferred_to_dropbox_failed)
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)
        ingest_status_api_client_mock.report_status.assert_called_once_with(expected_ingest_parameter)

    def test_set_ingest_as_transferred_failed_repository_raises_ingest_save_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.save.side_effect = IngestSaveException("test", "test")
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        with self.assertRaises(SetIngestAsTransferredFailedException):
            sut.set_ingest_as_transferred_failed(self.TEST_INGEST)

        ingest_status_api_client_mock.report_status.assert_not_called()

    def test_set_ingest_as_transferred_failed_api_client_raises_report_status_api_client_exception(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_stub = Mock(spec=IIngestStatusApiClient)
        ingest_status_api_client_stub.report_status.side_effect = ReportStatusApiClientException("test")

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_stub
        )

        with self.assertRaises(SetIngestAsTransferredFailedException):
            sut.set_ingest_as_transferred_failed(self.TEST_INGEST)

        expected_ingest_parameter = replace(self.TEST_INGEST, status=IngestStatus.transferred_to_dropbox_failed)
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)

    def test_process_ingest_repository_raises_ingest_save_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.save.side_effect = IngestSaveException("test", "test")
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        with self.assertRaises(ProcessIngestException):
            sut.process_ingest(self.TEST_INGEST)

        replace(self.TEST_INGEST, status=IngestStatus.processing_batch_ingest)
        ingest_status_api_client_mock.report_status.assert_not_called()

    def test_set_ingest_as_processed_happy_path(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        test_drs_url = "test"
        sut.set_ingest_as_processed(self.TEST_INGEST, test_drs_url)

        expected_ingest_parameter = replace(
            self.TEST_INGEST,
            drs_url=test_drs_url,
            status=IngestStatus.batch_ingest_successful
        )
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)
        ingest_status_api_client_mock.report_status.assert_called_once_with(expected_ingest_parameter)

    def test_set_ingest_as_processed_repository_raises_ingest_save_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.save.side_effect = IngestSaveException("test", "test")
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        with self.assertRaises(SetIngestAsProcessedException):
            sut.set_ingest_as_processed(self.TEST_INGEST, "test")

        ingest_status_api_client_mock.report_status.assert_not_called()

    def test_set_ingest_as_processed_api_client_raises_report_status_api_client_exception(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_stub = Mock(spec=IIngestStatusApiClient)
        ingest_status_api_client_stub.report_status.side_effect = ReportStatusApiClientException("test")

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_stub
        )

        test_drs_url = "test"
        with self.assertRaises(SetIngestAsProcessedException):
            sut.set_ingest_as_processed(self.TEST_INGEST, test_drs_url)

        expected_ingest_parameter = replace(
            self.TEST_INGEST,
            drs_url=test_drs_url,
            status=IngestStatus.batch_ingest_successful
        )
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)

    def test_set_ingest_as_processed_failed_happy_path(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        sut.set_ingest_as_processed_failed(self.TEST_INGEST)

        expected_ingest_parameter = replace(self.TEST_INGEST, status=IngestStatus.batch_ingest_failed)
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)
        ingest_status_api_client_mock.report_status.assert_called_once_with(expected_ingest_parameter)

    def test_set_ingest_as_processed_failed_repository_raises_ingest_save_exception(self) -> None:
        ingest_repository_stub = Mock(spec=IIngestRepository)
        ingest_repository_stub.save.side_effect = IngestSaveException("test", "test")
        ingest_status_api_client_mock = Mock(spec=IIngestStatusApiClient)

        sut = IngestService(
            ingest_repository=ingest_repository_stub,
            ingest_status_api_client=ingest_status_api_client_mock
        )

        with self.assertRaises(SetIngestAsProcessedFailedException):
            sut.set_ingest_as_processed_failed(self.TEST_INGEST)

        ingest_status_api_client_mock.report_status.assert_not_called()

    def test_set_ingest_as_processed_failed_api_client_raises_report_status_api_client_exception(self) -> None:
        ingest_repository_mock = Mock(spec=IIngestRepository)
        ingest_status_api_client_stub = Mock(spec=IIngestStatusApiClient)
        ingest_status_api_client_stub.report_status.side_effect = ReportStatusApiClientException("test")

        sut = IngestService(
            ingest_repository=ingest_repository_mock,
            ingest_status_api_client=ingest_status_api_client_stub
        )

        with self.assertRaises(SetIngestAsProcessedFailedException):
            sut.set_ingest_as_processed_failed(self.TEST_INGEST)

        expected_ingest_parameter = replace(self.TEST_INGEST, status=IngestStatus.batch_ingest_failed)
        ingest_repository_mock.save.assert_called_once_with(expected_ingest_parameter)
