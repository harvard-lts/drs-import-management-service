from typing import Tuple, Dict

from flask import request

from app.common.application.controllers.error_responses.error_response_serializer import ErrorResponseSerializer
from app.common.application.controllers.error_responses.transfer_ingest_error_response import \
    TransferIngestErrorResponse
from app.common.application.controllers.error_responses.unsupported_depositing_application_error_response import \
    UnsupportedDepositingApplicationErrorResponse
from app.containers import Services, Serializers
from app.ingest.domain.models.ingest.depositing_application import DepositingApplication
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.services.exceptions.transfer_ingest_exception import TransferIngestException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.domain.models.ingest.ingest_status import IngestStatus


class IngestPostController:

    def __init__(
            self,
            ingest_service: IngestService = Services.ingest_service(),
            error_response_serializer: ErrorResponseSerializer = Serializers.error_response_serializer()
    ) -> None:
        self.__ingest_service = ingest_service
        self.__error_response_serializer = error_response_serializer

    def __call__(self) -> Tuple[Dict, int]:
        package_id: str = request.json.get("package_id")
        s3_path: str = request.json.get("s3_path")
        s3_bucket_name: str = request.json.get("s3_bucket_name")
        admin_metadata: dict = request.json.get("admin_metadata")
        depositing_application_value: str = request.json.get("depositing_application")

        try:
            depositing_application = DepositingApplication(depositing_application_value)
        except ValueError:
            return self.__error_response_serializer.serialize(
                UnsupportedDepositingApplicationErrorResponse(depositing_application=depositing_application_value)
            )

        new_ingest = Ingest(
            package_id=package_id,
            s3_path=s3_path,
            s3_bucket_name=s3_bucket_name,
            destination_path=None,
            admin_metadata=admin_metadata,
            status=IngestStatus.pending_transfer_to_dropbox,
            depositing_application=DepositingApplication(depositing_application)
        )

        try:
            self.__ingest_service.transfer_ingest(new_ingest)
        except TransferIngestException as tie:
            return self.__error_response_serializer.serialize(TransferIngestErrorResponse(message=str(tie)))

        return {"package_id": new_ingest.package_id, "message": "Added to Queue"}, 202
