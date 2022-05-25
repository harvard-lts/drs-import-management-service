from app.ingest.domain.services.exceptions.process_service_exception import ProcessServiceException


class ProcessStatusMessageMissingFieldException(ProcessServiceException):
    def __init__(self, message_id: str, field_name: str) -> None:
        self.message = f"Process Status message with id {message_id} does not contain {field_name} field inside body"
        super().__init__(self.message)
