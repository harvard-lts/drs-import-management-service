from app.ingest.domain.services.exceptions.message_body_field_exception import MessageBodyFieldException


class MessageBodyMissingFieldException(MessageBodyFieldException):
    def __init__(self, message_id: str, field_name: str) -> None:
        self.message = f"Message with id {message_id} does not contain {field_name} field inside body"
        super().__init__(self.message)
