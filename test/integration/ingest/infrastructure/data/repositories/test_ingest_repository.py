import os
from dataclasses import replace

from app.common.infrastructure.data.repositories.db_connection_params \
    import DbConnectionParams
from app.ingest.infrastructure.data.repositories.ingest_repository \
    import IngestRepository
from test.integration.common.infrastructure.data.repositories. \
    mongo_integration_test_base import MongoIntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestIngestRepository(MongoIntegrationTestBase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_INGEST = create_ingest()
        cls.COLLECTION_NAME = "ingests"

    def test_save_new_ingest_happy_path(self) -> None:
        sut = IngestRepository()
        sut.save(self.TEST_INGEST)

        ingest_collection = self._get_database()[self.COLLECTION_NAME]
        actual_saved_ingest_dict = ingest_collection.find_one(
            {"package_id": self.TEST_INGEST.package_id})

        actual_package_id = actual_saved_ingest_dict["package_id"]
        expected_package_id = self.TEST_INGEST.package_id

        self.assertEqual(actual_package_id, expected_package_id)

    def test_save_existing_ingest_happy_path(self) -> None:
        self.__insert_test_ingest()

        sut = IngestRepository()
        new_test_s3_bucket_name = "new_test_s3_bucket_name"
        sut.save(replace(self.TEST_INGEST,
                         s3_bucket_name=new_test_s3_bucket_name))

        ingest_collection = self._get_database()[self.COLLECTION_NAME]

        actual_saved_ingests_count = ingest_collection.count_documents({})
        expected_saved_ingests_count = 1

        self.assertEqual(actual_saved_ingests_count,
                         expected_saved_ingests_count)

        actual_saved_ingest_dict = ingest_collection.find_one(
            {"package_id": self.TEST_INGEST.package_id})

        actual_package_id = actual_saved_ingest_dict["package_id"]
        expected_package_id = self.TEST_INGEST.package_id

        self.assertEqual(actual_package_id, expected_package_id)

        actual_s3_bucket_name = actual_saved_ingest_dict["s3_bucket_name"]
        expected_s3_bucket_name = new_test_s3_bucket_name

        self.assertEqual(actual_s3_bucket_name, expected_s3_bucket_name)

    def test_get_by_package_id_ingest_exists_happy_path(self) -> None:
        self.__insert_test_ingest()

        sut = IngestRepository()

        actual_ingest = sut.get_by_package_id(self.TEST_INGEST.package_id)
        expected_ingest = self.TEST_INGEST
        print(actual_ingest)
        print(expected_ingest)
        self.assertEqual(actual_ingest, expected_ingest)

    def test_get_by_package_id_ingest_does_not_exist_happy_path(self) -> None:
        sut = IngestRepository()

        actual_ingest = sut.get_by_package_id(self.TEST_INGEST.package_id)

        self.assertIsNone(actual_ingest)

    def _get_db_connection_params(self) -> DbConnectionParams:
        return DbConnectionParams(
            db_hosts=[os.getenv('MONGODB_HOST_1'), os.getenv('MONGODB_HOST_2'),
                      os.getenv('MONGODB_HOST_3')],
            db_port=int(os.getenv('MONGODB_PORT')),
            db_name=os.getenv('MONGODB_DB_NAME'),
            db_user=os.getenv('MONGODB_USER'),
            db_password=os.getenv('MONGODB_PASSWORD'),
        )

    def _get_db_collection_name(self) -> str:
        return self.COLLECTION_NAME

    def __insert_test_ingest(self) -> None:
        ingest_collection = self._get_database()[self.COLLECTION_NAME]
        ingest_collection.insert_one(
            {
                "package_id": self.TEST_INGEST.package_id,
                "s3_path": self.TEST_INGEST.s3_path,
                "s3_bucket_name": self.TEST_INGEST.s3_bucket_name,
                "fs_source_path": self.TEST_INGEST.fs_source_path,
                "fs_source_server": self.TEST_INGEST.fs_source_server,
                "admin_metadata": self.TEST_INGEST.admin_metadata,
                "status": self.TEST_INGEST.status.value,
                "depositing_application": 
                self.TEST_INGEST.depositing_application
            }
        )
