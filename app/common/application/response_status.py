from enum import auto

from app.common.auto_name_enum import AutoNameEnum


class ResponseStatus(AutoNameEnum):
    success = auto()
    pending = auto()
    failure = auto()
