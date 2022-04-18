from enum import auto

from app.common.auto_name_enum import AutoNameEnum


class DepositingApplication(AutoNameEnum):
    Dataverse = auto()
    ePADD = auto()
