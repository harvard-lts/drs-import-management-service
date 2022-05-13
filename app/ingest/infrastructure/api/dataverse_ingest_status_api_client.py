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
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.infrastructure.api.dataverse_ingest_message_factory import DataverseIngestMessageFactory
from app.ingest.infrastructure.api.dataverse_params_transformer import DataverseParamsTransformer
from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException


class DataverseIngestStatusApiClient(IIngestStatusApiClient):
    __API_ENDPOINT = "/api/datasets/submitDatasetVersionToArchive/:persistentId/{version}/status?persistentId=doi:{doi}"
    __API_REQUEST_MAX_RETRIES = 2

    def __init__(self, dataverse_params_transformer: DataverseParamsTransformer) -> None:
        self.__dataverse_params_transformer = dataverse_params_transformer

    @retry(
        stop=stop_after_attempt(__API_REQUEST_MAX_RETRIES),
        retry=retry_if_exception_type(ReportStatusApiClientException),
        reraise=True,
        before=before_log(logging.getLogger(), logging.INFO)
    )
    def report_status(self, ingest: Ingest) -> None:
        ingest_package_id = ingest.package_id

        logger = logging.getLogger()
        logger.info(
            "Reporting status " + ingest.status.value + " for package id " + ingest_package_id + " to Dataverse...")
        try:
            dataverse_base_url = os.getenv('DATAVERSE_BASE_URL')
            logger.debug("Dataverse base url: " + dataverse_base_url)

            doi, version = self.__dataverse_params_transformer.transform_package_id_to_dataverse_params(
                ingest_package_id
            )
            formatted_api_endpoint = self.__API_ENDPOINT.format(version=version, doi=doi)
            logger.debug("API endpoint: " + formatted_api_endpoint)

            request_body = self.__create_request_body(ingest)
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

    def __create_request_body(self, ingest: Ingest) -> str:
        dataverse_ingest_status = \
            self.__dataverse_params_transformer.transform_ingest_status_to_dataverse_ingest_status(ingest.status)
        dataverse_ingest_message_factory = DataverseIngestMessageFactory()
        dataverse_ingest_message = dataverse_ingest_message_factory.get_dataverse_ingest_message(ingest)
        return '{"status":"' + dataverse_ingest_status + '","message":"' + dataverse_ingest_message + '"}'

    def __create_request_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Dataverse-key": os.getenv('DATAVERSE_API_KEY')}
