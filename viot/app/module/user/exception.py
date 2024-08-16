from app.common.exception import BadRequestException


class UserNotFoundException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="User not found")


class UserEmailAlreadyExistsException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="A user with this email already exists")


class PasswordNotMatchException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="Password not match")
