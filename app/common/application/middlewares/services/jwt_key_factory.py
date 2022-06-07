import os
from typing import Optional

from app.common.application.middlewares.services.dataverse_jwt_key import DataverseJwtKey
from app.common.application.middlewares.services.epadd_jwt_key import EpaddJwtKey
from app.common.application.middlewares.services.jwt_key import JwtKey


class JwtKeyFactory:

    def get_jwt_key(self, key_id: str) -> Optional[JwtKey]:
        return {
            os.getenv('DATAVERSE_JWT_KID'): DataverseJwtKey(),
            os.getenv('EPADD_JWT_KID'): EpaddJwtKey()
        }.get(key_id, None)
