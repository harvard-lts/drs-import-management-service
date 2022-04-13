class TransformPackageIdException(Exception):
    def __init__(self, package_id: str, reason: str) -> None:
        self.message = f"There was an error while transforming package id {package_id} to Dataverse API params. " \
                       f"Reason was: {reason}"
        super().__init__(self.message)
