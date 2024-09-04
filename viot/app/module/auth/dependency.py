from collections.abc import Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import injector

from .constants import ViotUserRole
from .exception.auth_exception import (
    UnauthorizedException,
    UserDisabledException,
    UserNotVerifiedException,
    ViotRoleException,
)
from .model.user import User
from .repository.user_repository import UserRepository
from .utils.token_utils import AccessToken, parse_access_token

_http_bearer = HTTPBearer(auto_error=False)


@lru_cache
def get_user_repository() -> UserRepository:
    return injector.get(UserRepository)


async def get_access_token(
    *,
    header: Annotated[HTTPAuthorizationCredentials | None, Depends(_http_bearer)],
) -> AccessToken:
    """Get access token dependency"""
    if header is None:
        raise UnauthorizedException
    return parse_access_token(header.credentials)


async def get_current_user(
    *,
    access_token: Annotated[AccessToken, Depends(get_access_token)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """Get current user dependency"""
    user = await user_repository.find(id=access_token.user_id)
    if user is None:
        raise UnauthorizedException
    if user.disabled:
        raise UserDisabledException
    if user.email_verified_at is None:
        raise UserNotVerifiedException
    return user


def RequireGlobalRole(role: ViotUserRole) -> Callable[[User], User]:
    """
    Create a dependency that requires a specific Viot user role.

    This function returns a FastAPI dependency that checks if the current user
    has the specified role. If the user doesn't have the required role, it
    raises a ViotRoleException.


    Raises:
        ViotRoleException: If the user doesn't have the required role.

    Usage:
    ```python
        @app.get("/admin-only")
        async def admin_endpoint(user: User = RequireViotRole(ViotUserRole.ADMIN)):
            return {"message": "Welcome, admin!"}
    ```
    """

    async def require_viot_role(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role != role:
            raise ViotRoleException(role)
        return user

    return Depends(require_viot_role)


DependCurrentUser = Depends(get_current_user)
