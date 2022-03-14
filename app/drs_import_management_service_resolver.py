from connexion import Resolver, Resolution
from connexion.operations import AbstractOperation

from .ingest.application.controllers.ingest_post_controller import IngestPostController


class DrsImportManagementServiceResolver(Resolver):
    # TODO: Dependency Injection
    OPERATION_MAPPING = {
        "initiateIngest": IngestPostController(None)
    }

    def resolve(self, operation: AbstractOperation) -> Resolution:
        operation_id = self.resolve_operation_id(operation)
        operation_controller = self.OPERATION_MAPPING.get(operation_id)
        return Resolution(operation_controller, operation_id)
