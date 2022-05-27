from app.ingest.domain.services.exceptions.transfer_service_exception import TransferServiceException


class TransferStatusMessageMissingFieldException(TransferServiceException):
    def __init__(self, message_id: str, field_name: str) -> None:
        self.message = f"Transfer Status message with id {message_id} does not contain {field_name} field inside body"
        super().__init__(self.message)
