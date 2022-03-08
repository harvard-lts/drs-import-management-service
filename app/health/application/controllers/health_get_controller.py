from typing import Tuple


class HealthGetController:

    def __call__(self) -> Tuple[str, int]:
        return "OK!", 200
