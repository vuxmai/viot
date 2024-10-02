from uuid import UUID

from app.common.exception import BadRequestException

from ..constants import MAX_ROLES_PER_TEAM, TEAM_ROLE_OWNER


class RoleNameExistsInTeamException(BadRequestException):
    def __init__(self, role_name: str) -> None:
        super().__init__(
            code="ROLE_NAME_EXISTS_IN_TEAM",
            message=f"Role name {role_name} already exists in team",
        )


class RoleIdNotFoundException(BadRequestException):
    def __init__(self, role_id: int) -> None:
        super().__init__(
            code="ROLE_ID_NOT_FOUND",
            message=f"Role id {role_id} not found",
        )


class TeamRoleLimitException(BadRequestException):
    def __init__(self, team_id: UUID) -> None:
        super().__init__(
            code="TEAM_ROLE_LIMIT",
            message=(
                f"Team {team_id} has reached the limit of roles, "
                f"maximum is {MAX_ROLES_PER_TEAM}"
            ),
        )


class CannotModifyOwnerRoleException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(
            code="CANNOT_MODIFY_OWNER_ROLE",
            message=f"Cannot update or delete the {TEAM_ROLE_OWNER} role of the team",
        )
