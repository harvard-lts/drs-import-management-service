from app.common.application.controllers.error_responses.error_response import ErrorResponse


class TransferIngestErrorResponse(ErrorResponse):
    http_code = 500
    status_code = "TRANSFER_INGEST_ERROR"

    def __init__(self, package_id: str, message: str) -> None:
        self.package_id = package_id
        self.message = message
