"""
This module defines an IIngestStatusApiClient, which is a domain interface that
defines the necessary methods to implement by an ingest status api client.
"""

from abc import ABC, abstractmethod

from app.ingest.domain.models.ingest.ingest import Ingest


class IIngestStatusApiClient(ABC):

    @abstractmethod
    def report_status(self, ingest: Ingest) -> None:
        """
        Reports an ingest status to a remote API.

        :param ingest: Ingest to report its status
        :type ingest: Ingest

        :raises ReportStatusApiClientException
        """
