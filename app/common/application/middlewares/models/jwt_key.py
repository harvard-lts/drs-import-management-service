from dataclasses import dataclass


@dataclass
class JwtKey:
    issuer: str
    public_key_path: str
    depositing_application: str
