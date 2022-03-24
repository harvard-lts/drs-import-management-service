from connexion import Resolver, Resolution
from connexion.operations import AbstractOperation

from app.ingest.application.controllers.ingest_post_controller import IngestPostController


class DrsImportManagementServiceResolver(Resolver):
    OPERATION_MAPPING = {
        "initiateIngest": IngestPostController()
    }

    def resolve(self, operation: AbstractOperation) -> Resolution:
        operation_id = self.resolve_operation_id(operation)
        operation_controller = self.OPERATION_MAPPING.get(operation_id)
        return Resolution(operation_controller, operation_id)
