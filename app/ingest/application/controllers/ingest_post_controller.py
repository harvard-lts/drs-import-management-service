from typing import Tuple, Dict

from flask import request
import traceback
import json

from app.common.application.controllers.responses.error_response_serializer  \
    import ErrorResponseSerializer
from app.common.application.response_status import ResponseStatus
from app.containers import Services, Controllers
from app.ingest.application.controllers.responses. \
    transfer_ingest_error_response import TransferIngestErrorResponse
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.models.ingest.ingest_status import IngestStatus
from app.ingest.domain.services.exceptions.transfer_ingest_exception  \
    import TransferIngestException
from app.ingest.domain.services.ingest_service import IngestService
from app.ingest.infrastructure.api.dataverse_ingest_message_factory  \
    import DataverseIngestMessageFactory
import app.notifier.notifier as notifier


class IngestPostController:

    def __init__(
            self,
            error_response_serializer: ErrorResponseSerializer =
            Controllers.error_response_serializer(),
            ingest_service: IngestService = Services.ingest_service()
    ) -> None:
        self.__error_response_serializer = error_response_serializer
        self.__ingest_service = ingest_service

    def __call__(self) -> Tuple[Dict, int]:
        package_id: str = request.json.get("package_id")
        s3_path: str = request.json.get("s3_path")
        s3_bucket_name: str = request.json.get("s3_bucket_name")
        fs_source_path: str = request.json.get("fs_source_path")
        admin_metadata: dict = request.json.get("admin_metadata")
        depositing_application: str = request.json.get("depositing_application")

        if "dry_run" in request.json:
            dry_run: str = request.json.get("dry_run")
        else:
            dry_run = None

        new_ingest = Ingest(
            package_id=package_id,
            s3_path=s3_path,
            s3_bucket_name=s3_bucket_name,
            fs_source_path=fs_source_path,
            admin_metadata=admin_metadata,
            status=IngestStatus.pending_transfer_to_dropbox,
            depositing_application=depositing_application,
            drs_url=None,
            dry_run=dry_run
        )

        try:
            self.__ingest_service.transfer_ingest(new_ingest)
        except TransferIngestException as tie:
            data = {"package_id": package_id,
                    "s3_path": s3_path,
                    "s3_bucket_name": s3_bucket_name,
                    "fs_source_path": fs_source_path,
                    "admin_metadata": admin_metadata,
                    "depositing_application": depositing_application}
            msg = "Could not transfer ingest for {} package {}.  Error {}." \
                .format(depositing_application, package_id, str(tie))
            exception_msg = traceback.format_exc()
            body = msg + "\nData:" + json.dumps(data) + "\n" + exception_msg
            notifier.send_error_notification(str(tie), body)
            return self.__error_response_serializer.serialize(
                TransferIngestErrorResponse(message=str(tie))
            )  

        dataverse_ingest_status_factory = DataverseIngestMessageFactory()
        return {
                   "package_id": new_ingest.package_id,
                   "status": ResponseStatus.pending.value,
                   "status_code": None,
                   "message": dataverse_ingest_status_factory.get_dataverse_ingest_message(new_ingest)
               }, 202
