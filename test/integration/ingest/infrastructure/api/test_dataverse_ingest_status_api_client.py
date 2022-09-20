import os
from os.path import join, dirname

from requests import post, delete, get

from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_ingest_status_api_client import DataverseIngestStatusApiClient
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from test.integration.integration_test_base import IntegrationTestBase
from test.resources.ingest.ingest_factory import create_ingest


class TestDataverseIngestStatusApiClient(IntegrationTestBase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.API_DATAVERSE_CREATE_ENDPOINT = "/api/dataverses/root"
        cls.API_DATAVERSE_PUBLISH_ENDPOINT = "/api/dataverses/{collection_alias}/actions/:publish"
        cls.API_DATAVERSE_DELETE_ENDPOINT = "/api/dataverses/{collection_alias}"

        cls.API_DATASET_CREATE_ENDPOINT = "/api/dataverses/{collection_alias}/datasets"
        cls.API_DATASET_PUBLISH_ENDPOINT = "/api/datasets/:persistentId/actions/:publish?persistentId={persistent_id}&type=major&assureIsIndexed=true"
        cls.API_DATASET_DELETE_ENDPOINT = "/api/datasets/{dataset_id}/destroy"
        cls.API_DATASET_STATUS_ENDPOINT = "/api/datasets/{dataset_id}/{version}/archivalStatus"

        cls.TEST_DATAVERSE_ALIAS = "test_dataverse_alias"

    def setUp(self) -> None:
        super().setUp()
        self.__dataverse_base_url = os.getenv('DATAVERSE_BASE_URL')
        self.__persistent_id = None
        self.__dataset_id = None
        self.__create_test_resources()

    def tearDown(self) -> None:
        self.__delete_test_resources()

    def test_report_status_happy_path(self) -> None:
        test_package_id = self.__transform_persistent_id_to_dims_package_id()
        test_drs_url = "https://dataverse.org/"
        test_ingest = create_ingest(
            package_id=test_package_id,
            status=IngestStatus.batch_ingest_successful,
            drs_url=test_drs_url
        )

        sut = DataverseIngestStatusApiClient(DataverseParamsTransformer())
        sut.report_status(test_ingest)

        actual_status = self.__get_actual_dataset_status()
        expected_status = "success"

        self.assertEqual(actual_status, expected_status)

    def __transform_persistent_id_to_dims_package_id(self) -> str:
        package_id = self.__persistent_id.replace(":", ".").replace(".", "-").replace("/", "-") + "_v1_0"
        return package_id

    def __get_actual_dataset_status(self) -> str:
        get_dataset_status_api_endpoint = self.API_DATASET_STATUS_ENDPOINT.format(
            dataset_id=self.__dataset_id,
            version="1.0"
        )

        response = get(
            url=f"{self.__dataverse_base_url}{get_dataset_status_api_endpoint}",
            headers=self.__create_request_headers(),
        )

        response_json = response.json()
        return response_json['data']['status']

    def __create_test_resources(self):
        self.__create_test_dataverse()
        self.__publish_test_dataverse()
        self.__create_test_dataset()
        self.__publish_test_dataset()

    def __create_test_dataverse(self) -> None:
        with open(join(dirname(__file__), 'test_dataverse.json')) as file:
            request_body = file.read()

        post(
            url=f"{self.__dataverse_base_url}{self.API_DATAVERSE_CREATE_ENDPOINT}",
            data=request_body,
            headers=self.__create_request_headers(),
        )

    def __publish_test_dataverse(self) -> None:
        publish_dataverse_api_endpoint = self.API_DATAVERSE_PUBLISH_ENDPOINT.format(
            collection_alias=self.TEST_DATAVERSE_ALIAS
        )

        post(
            url=f"{self.__dataverse_base_url}{publish_dataverse_api_endpoint}",
            headers=self.__create_request_headers(),
        )

    def __create_test_dataset(self) -> None:
        create_dataset_api_endpoint = self.API_DATASET_CREATE_ENDPOINT.format(
            collection_alias=self.TEST_DATAVERSE_ALIAS
        )

        with open(join(dirname(__file__), 'test_dataset.json')) as file:
            request_body = file.read()

        response = post(
            url=f"{self.__dataverse_base_url}{create_dataset_api_endpoint}",
            data=request_body,
            headers=self.__create_request_headers(),
        )

        response_json = response.json()
        self.__persistent_id = response_json['data']['persistentId']
        self.__dataset_id = response_json['data']['id']

    def __publish_test_dataset(self) -> None:
        publish_dataset_api_endpoint = self.API_DATASET_PUBLISH_ENDPOINT.format(
            persistent_id=self.__persistent_id
        )

        post(
            url=f"{self.__dataverse_base_url}{publish_dataset_api_endpoint}",
            headers=self.__create_request_headers(),
        )

    def __delete_test_resources(self):
        self.__delete_test_dataset()
        self.__delete_test_dataverse()

    def __delete_test_dataset(self) -> None:
        delete_dataset_api_endpoint = self.API_DATASET_DELETE_ENDPOINT.format(
            dataset_id=self.__dataset_id
        )

        delete(
            url=f"{self.__dataverse_base_url}{delete_dataset_api_endpoint}",
            headers=self.__create_request_headers(),
        )

    def __delete_test_dataverse(self) -> None:
        delete_dataverse_api_endpoint = self.API_DATAVERSE_DELETE_ENDPOINT.format(
            collection_alias=self.TEST_DATAVERSE_ALIAS
        )

        delete(
            url=f"{self.__dataverse_base_url}{delete_dataverse_api_endpoint}",
            headers=self.__create_request_headers(),
        )

    def __create_request_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Dataverse-key": os.getenv('DATAVERSE_API_KEY')}
