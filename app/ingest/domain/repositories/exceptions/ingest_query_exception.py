class IngestQueryException(Exception):
    def __init__(self, package_id: str, reason: str) -> None:
        self.message = f"An error occurred while querying ingest with package id {package_id}. Reason was: {reason}"
        super().__init__(self.message)
