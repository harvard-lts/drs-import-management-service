from dataclasses import dataclass


@dataclass
class DbConnectionParams:
    db_hosts: list
    db_port: int
    db_name: str
    db_user: str
    db_password: str
