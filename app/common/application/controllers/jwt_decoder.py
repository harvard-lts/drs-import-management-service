import jwt


class JwtDecoder:
    ENCODING_ALGORITHM = "RS256"

    def __init__(self, public_jwt_key: str) -> None:
        self.__public_jwt_key = public_jwt_key

    def decode(self, encoded: str) -> dict:
        return jwt.decode(encoded, self.__public_jwt_key, algorithm=self.ENCODING_ALGORITHM)
