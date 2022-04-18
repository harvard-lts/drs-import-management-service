"""
This module defines a DataverseIngestStatusApiClient, an implementation of IIngestStatusApiClient which
includes the necessary logic to connect to a remote Dataverse instance API and report an ingest status.
"""

import os

from requests import post, exceptions

from app.ingest.domain.api.exceptions.report_status_api_client_exception import ReportStatusApiClientException
from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException


# TODO: Integration test
class DataverseIngestStatusApiClient(IIngestStatusApiClient):
    API_ENDPOINT = "/api/datasets/submitDataVersionToArchive/:persistentId/{version}/status?persistentId=doi:{doi}"

    def __init__(self, dataverse_params_transformer: DataverseParamsTransformer) -> None:
        self.__dataverse_params_transformer = dataverse_params_transformer

    def report_status(self, package_id: str, ingest_status: IngestStatus) -> None:
        try:
            doi, version = self.__dataverse_params_transformer.transform_package_id_to_dataverse_params(package_id)
            dataverse_base_url = os.getenv('DATAVERSE_BASE_URL')
            post(
                url=f"{dataverse_base_url}{self.API_ENDPOINT.format(version=version, doi=doi)}",
                data=self.__create_request_body(ingest_status),
                headers=self.__create_request_headers()
            )
        except (TransformPackageIdException, exceptions.ConnectionError) as e:
            raise ReportStatusApiClientException(str(e))

    def __create_request_body(self, ingest_status: IngestStatus) -> dict:
        return {
            "status": self.__dataverse_params_transformer.transform_ingest_status_to_response_status(ingest_status),
            # TODO: Send actual URL (success) or message (pending, error)
            "message": os.getenv('DATAVERSE_BASE_URL')
        }

    def __create_request_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Dataverse-key": os.getenv('DATAVERSE_API_KEY')}
