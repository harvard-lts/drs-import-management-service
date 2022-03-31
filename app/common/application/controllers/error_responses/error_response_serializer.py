from typing import Tuple, Dict

from app.common.application.controllers.error_responses.error_response import ErrorResponse


class ErrorResponseSerializer:

    def serialize(self, error_response: ErrorResponse) -> Tuple[Dict, int]:
        return {"message": error_response.message}, error_response.http_code
