from app.ingest.domain.services.exceptions.transfer_service_exception import TransferServiceException


class TransferStatusMessageHandlingException(TransferServiceException):
    def __init__(self, message_id: str, reason: str) -> None:
        self.message = f"There was an error when handling Transfer Status message with id {message_id}. " \
                       f"Reason was: {reason}"
        super().__init__(self.message)
