from abc import ABC, abstractmethod
from typing import Optional

from app.ingest.domain.models.ingest.ingest import Ingest


class IIngestRepository(ABC):

    @abstractmethod
    def save(self, ingest: Ingest) -> None:
        """
        Saves an ingest.

        :param ingest: Ingest to save
        :type ingest: Ingest
        """

    @abstractmethod
    def get_by_package_id(self, package_id: str) -> Optional[Ingest]:
        """
        Retrieves and returns an ingest given a package id if the ingest exists.
        If the ingest does not exist, returns None.

        :param package_id: Ingest package id
        :type package_id: str
        """
