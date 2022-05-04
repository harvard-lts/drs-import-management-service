from typing import Tuple

from app.ingest.application.controllers.services.git_service import GitService


class HealthGetController:

    def __call__(self) -> Tuple[str, int]:
        return "OK!" + " " + GitService().get_commit_hash(), 200
