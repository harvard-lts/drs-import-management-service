from app.ingest.domain.services.exceptions.process_service_exception import ProcessServiceException


class ProcessStatusMessageHandlingException(ProcessServiceException):
    def __init__(self, message_id: str, reason: str) -> None:
        self.message = f"There was an error when handling Process Status message with id {message_id}. " \
                       f"Reason was: {reason}"
        super().__init__(self.message)
