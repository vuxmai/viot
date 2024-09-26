from app.common.exception import BadRequestException


class RoleNameExistsInTeamException(BadRequestException):
    def __init__(self, role_name: str) -> None:
        super().__init__(
            code="ROLE_NAME_EXISTS_IN_TEAM",
            message=f"Role name {role_name} already exists in team",
        )
