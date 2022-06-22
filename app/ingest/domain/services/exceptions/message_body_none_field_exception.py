from app.ingest.domain.services.exceptions.message_body_field_exception import MessageBodyFieldException


class MessageBodyNoneFieldException(MessageBodyFieldException):
    def __init__(self, message_id: str, field_name: str) -> None:
        self.message = f"Message with id {message_id} has None value for field {field_name} inside body"
        super().__init__(self.message)
