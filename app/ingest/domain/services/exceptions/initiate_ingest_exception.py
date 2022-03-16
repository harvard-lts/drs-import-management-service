class InitiateIngestException(Exception):
    def __init__(self, reason: str) -> None:
        self.message = f"An error occurred while initiating ingest. Reason was: {reason}"
        super().__init__(self.message)
