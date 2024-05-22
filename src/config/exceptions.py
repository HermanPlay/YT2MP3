class AlreadyExistsError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class FileTooLarge(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
