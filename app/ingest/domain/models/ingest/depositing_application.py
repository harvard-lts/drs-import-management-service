from enum import auto

from app.common.domain.auto_name_enum import AutoNameEnum


class DepositingApplication(AutoNameEnum):
    Dataverse = auto()
    ePADD = auto()
