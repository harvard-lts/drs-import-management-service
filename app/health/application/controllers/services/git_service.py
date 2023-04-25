import logging

from git import Repo, GitError

from app.health.application.controllers.services.exceptions.get_current_commit_hash_exception import \
    GetCurrentCommitHashException


class GitService:
    __PATH_TO_REPO = "/home/dimsuser"

    def get_current_commit_hash(self) -> str:
        """
        Retrieves current DIMS repository commit hash.

        :raises GetCurrentCommitHashException
        """
        logger = logging.getLogger('dims')
        try:
            logger.info("Obtaining current git commit hash...")
            repo = Repo(self.__PATH_TO_REPO)
            commit_hash = repo.git.rev_parse("HEAD")
            logger.info("Current git commit hash: " + commit_hash)
            return commit_hash
        except GitError as ge:
            logger.error(str(ge))
            raise GetCurrentCommitHashException(str(ge))
