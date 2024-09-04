from app.common.exception import BadRequestException, NotFoundException, PermissionDeniedException


class TeamNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(message="Team not found")


class TeamSlugAlreadyExistsException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="Team slug already exists")


class TeamPermissionDeniedException(PermissionDeniedException):
    def __init__(self) -> None:
        super().__init__(message="User are not allowed to access this team")


class InsufficientTeamRoleException(PermissionDeniedException):
    def __init__(self, role: str) -> None:
        super().__init__(
            message=f"User role {role} does not have permission to perform this action"
        )
