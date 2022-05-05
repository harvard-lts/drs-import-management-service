from typing import Tuple

from app.containers import Controllers
from app.health.application.controllers.services.exceptions.get_current_commit_hash_exception import \
    GetCurrentCommitHashException
from app.health.application.controllers.services.git_service import GitService


class HealthGetController:

    def __init__(
            self,
            git_service: GitService = Controllers.git_service()
    ) -> None:
        self.__git_service = git_service

    def __call__(self) -> Tuple[str, int]:
        try:
            return "OK!" + " " + self.__git_service.get_current_commit_hash(), 200
        except GetCurrentCommitHashException as e:
            # TODO: Actual response
            return "NO OK!" + " " + str(e), 500
