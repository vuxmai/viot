from app.common.exception import BadRequestException, NotFoundException


class TeamInvitationNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(message="Team invitation not found")


class TeamInvitationExpiredException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(message="Team invitation expired")


class TeamInvitationRoleNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(message="Team invitation role not found")
