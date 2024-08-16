from app.common.exception import NotFoundException


class TeamInvitationNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(message="Team invitation not found")
