from app.ingest.domain.services.exceptions.message_body_missing_field_exception import MessageBodyMissingFieldException
from app.ingest.domain.services.exceptions.message_body_none_field_exception import \
    MessageBodyNoneFieldException


class MessageBodyTransformer:

    def get_message_body_field_value(self, field_name: str, message_body: dict, message_id: str) -> str:
        try:
            field_value = message_body[field_name]
        except KeyError as e:
            raise MessageBodyMissingFieldException(message_id, str(e))

        if field_value is None:
            raise MessageBodyNoneFieldException(message_id, field_name)

        return field_value
