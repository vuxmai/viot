from app.common.exception import (
    BadRequestException,
    PermissionDeniedException,
    UnauthorizedException,
)


# Authentication
class InvalidCredentialsException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="The provided credentials are incorrect",
        )


# Authorization
class UserNotVerifiedException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(message="Your email address has not been verified")


class UserDisabledException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(message="Your account has been disabled")


# Global role
class ViotRoleException(PermissionDeniedException):
    def __init__(self, role: str) -> None:
        super().__init__(message=f"This action requires a global role of {role}")


# Verify email
class InvalidVerifyEmailTokenException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="The provided verify email token is invalid")


# Reset password
class InvalidResetPasswordTokenException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="The provided reset password token is invalid")


class ResetPasswordTokenExpiredException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="The provided reset password token has expired")


class DuplicatePasswordException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="New password must be different from the current password")
