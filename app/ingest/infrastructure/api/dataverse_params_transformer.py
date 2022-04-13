from typing import Tuple

from app.ingest.infrastructure.api.exceptions.transform_package_id_exception import TransformPackageIdException


class DataverseParamsTransformer:

    def transform_package_id_to_dataverse_params(self, package_id: str) -> Tuple[str, str]:
        try:
            # Removing "doi-" prefix from the package_id
            formatted_package_id = package_id[4:]

            # Replacing first "-" occurrence by "."
            formatted_package_id = formatted_package_id.replace("-", ".", 1)

            # Replacing all "-" occurrences by "/"
            formatted_package_id = formatted_package_id.replace("-", "/")

            # Splitting the resulting string from ".v"
            formatted_package_id = formatted_package_id.split(".v")

            doi = formatted_package_id[0].upper()
            version = formatted_package_id[1]

            return doi, version

        except IndexError as ie:
            raise TransformPackageIdException(package_id, str(ie))
