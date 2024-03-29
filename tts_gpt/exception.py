class CustomHttpException(Exception):
    def __init__(self, code: int, message: str, log: str) -> None:
        self.code = code
        self.message = message
        self.log = log
        self.error = None

class TTSError(CustomHttpException):
    def __init__(
            self, code: int, message: str, log: str, err: Exception = None
            ) -> None:
        super().__init__(code, message, log)
        self.error = err