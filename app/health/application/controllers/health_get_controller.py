from typing import Tuple

from app.ingest.application.controllers.services.git_service import GitService
from app.containers import Controllers


class HealthGetController:

    def __init__(
            self,
            git_service: GitService = Controllers.git_service()
    ) -> None:
        self.__git_service = git_service

    def __call__(self) -> Tuple[str, int]:
        return "OK!" + " " + self.__git_service.get_commit_hash(), 200
