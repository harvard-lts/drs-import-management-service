from dataclasses import dataclass


@dataclass
class DbConnectionParams:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
