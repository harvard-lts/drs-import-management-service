import os
from typing import Optional

from app.common.application.middlewares.services.jwt_key import JwtKey


class JwtKeyFactory:

    def get_jwt_key(self, key_id: str) -> Optional[JwtKey]:
        dataverse_jwt_kid = os.getenv('DATAVERSE_JWT_KID')
        return {
            dataverse_jwt_kid: JwtKey(
                id=dataverse_jwt_kid,
                issuer=os.getenv('DATAVERSE_JWT_ISSUER'),
                public_key_path=os.getenv('DATAVERSE_JWT_PUBLIC_KEY_FILE_PATH')
            )
        }.get(key_id, None)
