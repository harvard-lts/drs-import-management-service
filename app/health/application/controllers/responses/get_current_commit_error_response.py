from app.common.application.controllers.responses.error_response import ErrorResponse


class GetCurrentCommitErrorResponse(ErrorResponse):
    http_code = 500
    status_code = "GET_CURRENT_COMMIT_ERROR"

    def __init__(self, message: str) -> None:
        self.message = message
