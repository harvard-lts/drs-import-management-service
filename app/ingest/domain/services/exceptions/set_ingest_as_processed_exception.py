from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException


class SetIngestAsProcessedException(IngestServiceException):
    def __init__(self, package_id: str, reason: str) -> None:
        self.message = f"There was an error when setting ingest with package id {package_id} as processed. Reason was: {reason}"
        super().__init__(self.message)
