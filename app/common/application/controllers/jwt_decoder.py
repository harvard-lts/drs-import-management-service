import jwt


class JwtDecoder:
    ENCODING_ALGORITHM = "RS256"

    def __init__(self, public_jwt_key: str) -> None:
        self.__public_jwt_key = public_jwt_key

    def decode(self, encoded: str) -> dict:
        return jwt.decode(
            jwt=encoded,
            key=self.__public_jwt_key,
            algorithms=[self.ENCODING_ALGORITHM]
        )
