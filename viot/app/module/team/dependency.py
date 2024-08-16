from functools import lru_cache
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from fastapi.params import Path

from app.container import injector
from app.module.auth.dependency import DependCurrentUser
from app.module.user.model import User

from .constant import TeamRole
from .exception import InsufficientTeamRoleException, TeamPermissionDeniedException
from .repository import UserTeamRepository


@lru_cache
def get_user_team_repository() -> UserTeamRepository:
    return injector.get(UserTeamRepository)


def RequireAnyTeamRole(roles: set[TeamRole] | TeamRole) -> Any:
    """
    A dependency that ensures the current user has at least one of the specified team roles.

    This function creates a FastAPI dependency that checks if the authenticated user has any of the
    required roles for a given team. It can be used to protect routes that require specific team
    permissions.

    Returns:
        Depends: A FastAPI dependency that performs the role check.

    Raises:
        TeamPermissionDeniedException: If the user is not a member of the team.
        InsufficientTeamRoleException: If the user's role is not in the set of allowed roles.

    Usage:
        ```python
        @app.get("/{group_id}/sensitive-data", dependencies=[RequireAnyTeamRole(TeamRole.ADMIN)])
        async def get_sensitive_data():
            # Only team admins can access this endpoint
            ...
        ```
    """
    if isinstance(roles, TeamRole):
        roles = {roles}

    async def validate_permission(
        user_team_repository: Annotated[UserTeamRepository, Depends(get_user_team_repository)],
        current_user: Annotated[User, DependCurrentUser],
        team_id: Annotated[UUID, Path(...)],
    ) -> None:
        role = await user_team_repository.find_role_name(current_user.id, team_id)
        if role is None:
            raise TeamPermissionDeniedException

        if role not in roles:
            raise InsufficientTeamRoleException(role)

    return Depends(validate_permission)
