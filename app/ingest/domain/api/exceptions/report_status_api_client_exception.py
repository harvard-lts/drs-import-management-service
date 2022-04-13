class ReportStatusApiClientException(Exception):
    def __init__(self, reason: str) -> None:
        message = f"An error occurred while reporting ingest status to remote API. Reason was {reason}"
        super().__init__(message)
