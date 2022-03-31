from app.common.application.controllers.error_responses.error_response import ErrorResponse


class TransferIngestErrorResponse(ErrorResponse):
    http_code = 500

    def __init__(self, message: str):
        self.message = message
