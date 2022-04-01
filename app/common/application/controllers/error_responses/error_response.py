from abc import ABC


class ErrorResponse(ABC):
    http_code: int
    status_code: str
    message: str
