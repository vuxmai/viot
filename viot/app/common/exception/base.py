from .constant import MessageError


class ViotException(Exception):
    pass


class ViotHttpException(ViotException):
    STATUS_CODE = 500

    def __init__(
        self,
        code: str = MessageError.INTERNAL_SERVER_ERROR,
        message: str = "Something went wrong",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.headers = headers
        super().__init__(message)


class BadRequestException(ViotHttpException):
    STATUS_CODE = 400

    def __init__(
        self, *, code: str = MessageError.BAD_REQUEST, message: str = "Bad request"
    ) -> None:
        super().__init__(code=code, message=message)


class UnauthorizedException(ViotHttpException):
    STATUS_CODE = 401

    def __init__(
        self, *, code: str = MessageError.UNAUTHORIZED, message: str = "Unauthorized"
    ) -> None:
        super().__init__(
            code=code,
            message=message,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedException(ViotHttpException):
    STATUS_CODE = 403

    def __init__(
        self, *, code: str = MessageError.PERMISSION_DENIED, message: str = "Permission denied"
    ) -> None:
        super().__init__(code=code, message=message)


class NotFoundException(ViotHttpException):
    STATUS_CODE = 404

    def __init__(
        self, *, code: str = MessageError.NOT_FOUND, message: str = "Resource not found"
    ) -> None:
        super().__init__(code=code, message=message)
