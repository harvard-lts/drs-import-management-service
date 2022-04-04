from app.common.application.controllers.responses.error_responses.error_response import ErrorResponse


class TransferIngestErrorResponse(ErrorResponse):
    http_code = 500
    status_code = "TRANSFER_INGEST_ERROR"

    def __init__(self, message: str) -> None:
        self.message = message
