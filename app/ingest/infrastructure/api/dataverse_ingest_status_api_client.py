"""
This module defines a DataverseIngestStatusApiClient, an implementation of IIngestStatusApiClient which
includes the necessary logic to connect to a remote Dataverse instance API and report an ingest status.
"""

import logging
import os

from requests import exceptions, put, HTTPError
from tenacity import retry_if_exception_type, stop_after_attempt, retry, before_log

from app.ingest.domain.api.exceptions.report_status_api_client_exception import ReportStatusApiClientException
from app.ingest.domain.api.ingest_status_api_client import IIngestStatusApiClient
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException


# TODO: Integration tests
class DataverseIngestStatusApiClient(IIngestStatusApiClient):
    __API_ENDPOINT = "/api/datasets/submitDatasetVersionToArchive/:persistentId/{version}/status?persistentId=doi:{doi}"
    __API_REQUEST_MAX_RETRIES = 2

    def __init__(self, dataverse_params_transformer: DataverseParamsTransformer) -> None:
        self.__dataverse_params_transformer = dataverse_params_transformer

    @retry(
        stop=stop_after_attempt(__API_REQUEST_MAX_RETRIES),
        retry=retry_if_exception_type(ReportStatusApiClientException),
        reraise=True,
        before=before_log(logging.getLogger(), logging.DEBUG)
    )
    def report_status(self, package_id: str, ingest_status: IngestStatus) -> None:
        logger = logging.getLogger()
        logger.debug("Reporting status " + ingest_status.value + " for package id " + package_id + " to Dataverse...")
        try:
            dataverse_base_url = os.getenv('DATAVERSE_BASE_URL')
            logger.debug("Dataverse base url: " + dataverse_base_url)

            doi, version = self.__dataverse_params_transformer.transform_package_id_to_dataverse_params(package_id)
            formatted_api_endpoint = self.__API_ENDPOINT.format(version=version, doi=doi)
            logger.debug("API endpoint: " + formatted_api_endpoint)

            request_body = self.__create_request_body(ingest_status)
            logger.debug("Request body: " + request_body)

            logger.debug("Executing PUT operation...")
            response = put(
                url=f"{dataverse_base_url}{formatted_api_endpoint}",
                data=request_body,
                headers=self.__create_request_headers(),
            )
            response.raise_for_status()
        except (TransformPackageIdException, exceptions.ConnectionError, HTTPError) as e:
            raise ReportStatusApiClientException(str(e))

    def __create_request_body(self, ingest_status: IngestStatus) -> str:
        # TODO: Send actual URL (for success) or message (for pending or error)
        return '{"status":"' \
               + self.__dataverse_params_transformer.transform_ingest_status_to_dataverse_ingest_status(ingest_status) \
               + '","message":"https://dataverse.harvard.edu/"}'

    def __create_request_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Dataverse-key": os.getenv('DATAVERSE_API_KEY')}
