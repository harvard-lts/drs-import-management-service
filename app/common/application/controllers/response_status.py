from enum import auto

from app.common.domain.auto_name_enum import AutoNameEnum


class ResponseStatus(AutoNameEnum):
    success = auto()
    pending = auto()
    failure = auto()
