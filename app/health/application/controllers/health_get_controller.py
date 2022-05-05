from typing import Tuple

from healthcheck import HealthCheck

from app.containers import Controllers
from app.health.application.controllers.services.exceptions.get_current_commit_hash_exception import \
    GetCurrentCommitHashException
from app.health.application.controllers.services.git_service import GitService
from app.health.infrastructure.compound_connectivity_service import CompoundConnectivityService


class HealthGetController:

    def __init__(
            self,
            git_service: GitService = Controllers.git_service()
    ) -> None:
        self.__git_service = git_service

    def __call__(self) -> Tuple[str, int]:
        health_check = HealthCheck()

        try:
            current_commit_hash = self.__git_service.get_current_commit_hash()
        except GetCurrentCommitHashException as e:
            # TODO: Actual response
            return "NO OK!" + " " + str(e), 500

        self.__add_connectivity_checkers(health_check)
        self.__add_application_section(current_commit_hash, health_check)

        return health_check.run()

    def __add_connectivity_checkers(self, health_check) -> None:
        compound_connectivity_service = CompoundConnectivityService()
        compound_connectivity_service.create_connectivity_check(health_check)

    def __add_application_section(self, current_commit_hash, health_check) -> None:
        health_check.add_section(
            "application",
            {
                "maintainer": "Harvard Library Technology Services",
                "git_repository": "https://github.com/harvard-lts/drs-import-management-service",
                "code_version": {
                    "commit_hash": current_commit_hash,
                }
            }
        )
