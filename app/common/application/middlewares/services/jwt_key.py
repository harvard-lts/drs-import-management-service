from dataclasses import dataclass


@dataclass
class JwtKey:
    id: str
    issuer: str
    public_key_path: str
