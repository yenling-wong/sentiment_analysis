class ProcessingFailedError(Exception):
    def __init__(self, message="Model failed to process data"):
        self.message = message
        super().__init__(self.message)