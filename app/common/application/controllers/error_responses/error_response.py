from abc import ABC


class ErrorResponse(ABC):
    http_code: int
    message: str
