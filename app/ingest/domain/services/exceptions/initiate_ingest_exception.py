class InitiateIngestException(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(f"An error occurred while initiating ingest. Reason was: {reason}")
