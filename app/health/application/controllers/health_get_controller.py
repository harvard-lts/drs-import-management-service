from typing import Any, Tuple

from healthcheck import HealthCheck

from app.common.application.controllers.responses.error_response_serializer import ErrorResponseSerializer
from app.containers import Controllers
from app.health.application.controllers.responses.get_current_commit_error_response import GetCurrentCommitErrorResponse
from app.health.application.controllers.services.exceptions.get_current_commit_hash_exception import \
    GetCurrentCommitHashException
from app.health.application.controllers.services.git_service import GitService
from app.health.infrastructure.connectivity_service import ConnectivityService


class HealthGetController:
    __APPLICATION_MAINTAINER = "Harvard Library Technology Services"
    __APPLICATION_GIT_REPOSITORY = "https://github.com/harvard-lts/drs-import-management-service"

    def __init__(
            self,
            error_response_serializer: ErrorResponseSerializer = Controllers.error_response_serializer(),
            connectivity_service: ConnectivityService = Controllers.get_connectivity_service(),
            git_service: GitService = Controllers.git_service()
    ) -> None:
        self.__error_response_serializer = error_response_serializer
        self.__connectivity_service = connectivity_service
        self.__git_service = git_service

    def __call__(self) -> Any:
        try:
            current_commit_hash = self.__git_service.get_current_commit_hash()
        except GetCurrentCommitHashException as e:
            return self.__error_response_serializer.serialize(
                GetCurrentCommitErrorResponse(message=str(e))
            )

        health_check = HealthCheck(success_ttl=None, failed_ttl=None)

        self.__add_application_section(current_commit_hash, health_check)
        self.__connectivity_service.create_connectivity_check(health_check)

        return self.__execute_health_check(health_check)

    def __add_application_section(self, current_commit_hash: str, health_check: HealthCheck) -> None:
        health_check.add_section(
            "application",
            {
                "maintainer": self.__APPLICATION_MAINTAINER,
                "git_repository": self.__APPLICATION_GIT_REPOSITORY,
                "code_version": {
                    "commit_hash": current_commit_hash,
                }
            }
        )

    def __execute_health_check(self, health_check: HealthCheck) -> Tuple[str, int, dict]:
        return health_check.run()
