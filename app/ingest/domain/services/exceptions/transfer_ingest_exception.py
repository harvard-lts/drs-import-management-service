from app.ingest.domain.services.exceptions.ingest_service_exception import IngestServiceException


class TransferIngestException(IngestServiceException):
    def __init__(self, package_id: str, reason: str) -> None:
        self.message = f"There was an error when transferring ingest with package id {package_id}. Reason was: {reason}"
        super().__init__(self.message)
