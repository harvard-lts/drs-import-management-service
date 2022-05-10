from app.health.infrastructure.dataverse.services.dataverse_connectivity_service import DataverseConnectivityService
from test.integration.integration_test_base import IntegrationTestBase


class TestDataverseConnectivityService(IntegrationTestBase):

    def test_check_dataverse_connection_happy_path(self) -> None:
        sut = DataverseConnectivityService()

        actual_result_status, actual_result_message = sut.check_dataverse_connection()

        self.assertTrue(actual_result_status)
        expected_result_message = "Dataverse connection OK"
        self.assertEqual(actual_result_message, expected_result_message)
