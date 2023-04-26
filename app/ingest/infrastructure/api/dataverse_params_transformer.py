"""
This module defines a DataverseParamsTransformer, which includes the
operations to transform parameters to match Dataverse API specification.
"""

from typing import Tuple

from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.infrastructure.api.dataverse_ingest_status import DataverseIngestStatus
from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException


class DataverseParamsTransformer:

    def transform_package_id_to_dataverse_params(self, package_id: str) -> Tuple[str, str]:
        """
        Transforms a package id to a tuple of Dataverse 'doi' and 'version' parameters.

        E.g., the package id 'doi-10-5072-fk2-e6cmkr_v1_18' will result in a tuple of '10.5072/FK2/E6CMKR' and '1.18'

        :param package_id: Source package id to generate Dataverse parameters
        :type package_id: str

        :raises TransformPackageIdException
        """
        try:
            # Removing "doi-" prefix from the package_id
            formatted_package_id = package_id[4:]

            # Replacing first "-" occurrence by "."
            formatted_package_id = formatted_package_id.replace("-", ".", 1)

            # Replacing all "-" occurrences by "/"
            formatted_package_id = formatted_package_id.replace("-", "/")

            # Splitting the resulting string from "_v"
            formatted_package_id = formatted_package_id.split("_v")

            doi = formatted_package_id[0].upper()

            # Replacing "_" occurrences by "." in version number
            version = formatted_package_id[1].replace("_", ".")

            return doi, version

        except IndexError as ie:
            raise TransformPackageIdException(package_id, str(ie)) from ie

    def transform_ingest_status_to_dataverse_ingest_status(self, ingest_status: IngestStatus) -> str:
        """
        Transforms an ingest status to a Dataverse ingest status.

        :param ingest_status: Source ingest status
        :type ingest_status: IngestStatus
        """
        if ingest_status == IngestStatus.batch_ingest_successful:
            return DataverseIngestStatus.success.value
        elif ingest_status == IngestStatus.transferred_to_dropbox_failed \
                or ingest_status == IngestStatus.batch_ingest_failed:
            return DataverseIngestStatus.failure.value
        return DataverseIngestStatus.pending.value
