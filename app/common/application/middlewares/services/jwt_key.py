from abc import ABC

from app.common.domain.models.depositing_application import DepositingApplication


class JwtKey(ABC):
    issuer: str
    public_key_path: str
    depositing_application: DepositingApplication
