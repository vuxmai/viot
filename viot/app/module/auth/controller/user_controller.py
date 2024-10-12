from typing import Annotated

from classy_fastapi import delete, get, patch, put
from fastapi import Body
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.team.dto.team_dto import TeamWithRoleAndPermissionsDto
from app.module.team.service.team_service import TeamService

from ..dependency import DependCurrentUser
from ..dto.user_dto import ChangePasswordDto, UserDto, UserUpdateDto, UserWithTeamsDto
from ..model.user import User
from ..service.user_service import UserService


class UserController(Controller):
    @inject
    def __init__(self, user_service: UserService, team_service: TeamService):
        super().__init__(prefix="/users", tags=["Users"], dependencies=[DependSession])
        self._user_service = user_service
        self._team_service = team_service

    @get(
        "/me",
        summary="Get current user",
        status_code=200,
        responses={200: {"model": UserWithTeamsDto}},
    )
    async def get_user(
        self, *, current_user: Annotated[User, DependCurrentUser]
    ) -> JSONResponse[UserWithTeamsDto]:
        """Get current user"""
        teams = await self._team_service.get_teams_with_role_by_user_id(user_id=current_user.id)
        return JSONResponse(
            content=UserWithTeamsDto(**current_user.to_dict(), teams=teams), status_code=200
        )

    @get(
        "/me/teams",
        summary="Get current user's teams",
        status_code=200,
        responses={200: {"model": list[TeamWithRoleAndPermissionsDto]}},
        deprecated=True,
    )
    async def get_teams(
        self, *, current_user: Annotated[User, DependCurrentUser]
    ) -> JSONResponse[list[TeamWithRoleAndPermissionsDto]]:
        """Get current user's teams"""
        return JSONResponse(
            content=await self._team_service.get_teams_with_role_by_user_id(
                user_id=current_user.id
            ),
            status_code=200,
        )

    @patch("/me", summary="Update user", status_code=200, responses={200: {"model": UserDto}})
    async def update_user(
        self,
        *,
        current_user: Annotated[User, DependCurrentUser],
        user_update_dto: Annotated[UserUpdateDto, Body(...)],
    ) -> JSONResponse[UserDto]:
        """Update current user"""
        return JSONResponse(
            content=await self._user_service.update_user(
                user_id=current_user.id, user_update_dto=user_update_dto
            ),
            status_code=200,
        )

    @put(
        "/me/change-password",
        summary="Change password",
        status_code=204,
    )
    async def change_password(
        self,
        *,
        current_user: Annotated[User, DependCurrentUser],
        change_password_dto: Annotated[ChangePasswordDto, Body(...)],
    ) -> JSONResponse[None]:
        """Change current user's password"""
        await self._user_service.change_password(
            user_id=current_user.id, change_password_dto=change_password_dto
        )
        return JSONResponse.no_content()

    @delete(
        "/me",
        summary="Delete current user",
        status_code=204,
    )
    async def delete_current_user(
        self, *, current_user: Annotated[User, DependCurrentUser]
    ) -> JSONResponse[None]:
        """Delete current user"""
        await self._user_service.delete_user_by_id(user_id=current_user.id)
        return JSONResponse.no_content()
