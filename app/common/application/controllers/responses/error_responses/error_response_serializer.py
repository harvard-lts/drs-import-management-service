from typing import Tuple, Dict

from app.common.application.controllers.responses.error_responses.error_response import ErrorResponse
from app.common.application.controllers.responses.response_status import ResponseStatus


class ErrorResponseSerializer:

    def serialize(self, error_response: ErrorResponse) -> Tuple[Dict, int]:
        return {
                   "status": ResponseStatus.failure.value,
                   "status_code": error_response.status_code,
                   "message": error_response.message
               }, error_response.http_code
