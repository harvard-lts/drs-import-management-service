"""
This module defines an IIngestStatusApiClient, which is a domain interface that
defines the necessary methods to implement by an ingest status api client.
"""

from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest_status import IngestStatus


class IIngestStatusApiClient(ABC):

    @abstractmethod
    def report_status(self, package_id: str, ingest_status: IngestStatus) -> None:
        """
        Reports an ingest status to a remote API.

        :param package_id: Package id of the source ingest to report its status
        :type package_id: str
        :param ingest_status: Ingest status of the source ingest to report
        :type ingest_status: IngestStatus

        :raises ReportStatusApiClientException
        """
