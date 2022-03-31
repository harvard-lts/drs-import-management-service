from abc import ABC


class ErrorResponse(ABC):
    package_id: str
    http_code: int
    status_code: str
    message: str
