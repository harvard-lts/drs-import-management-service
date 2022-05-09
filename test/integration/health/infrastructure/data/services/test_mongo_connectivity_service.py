from app.health.infrastructure.data.services.mongo_connectivity_service import MongoConnectivityService
from test.integration.integration_test_base import IntegrationTestBase


class TestMongoConnectivityService(IntegrationTestBase):

    def test_check_mongo_connection_happy_path(self) -> None:
        sut = MongoConnectivityService()

        actual_result_status, actual_result_message = sut.check_mongo_connection()

        self.assertTrue(actual_result_status)
        expected_result_message = "MongoDB connection OK"
        self.assertEqual(actual_result_message, expected_result_message)
