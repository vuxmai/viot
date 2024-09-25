from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, patch, post
from fastapi.params import Body, Path
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.auth.dependency import DependCurrentUser
from app.module.auth.model.user import User

from ..dto.team_dto import TeamCreateDto, TeamDto, TeamUpdateDto
from ..service.team_service import TeamService


class TeamController(Controller):
    @inject
    def __init__(self, team_service: TeamService):
        super().__init__(prefix="/teams", tags=["Teams"], dependencies=[DependSession])
        self._team_service = team_service

    @post("", summary="Create a team", status_code=201, responses={201: {"model": TeamDto}})
    async def create_team(
        self,
        *,
        current_user: Annotated[User, DependCurrentUser],
        team_create_dto: Annotated[TeamCreateDto, Body(...)],
    ) -> JSONResponse[TeamDto]:
        """Create a team"""
        return JSONResponse(
            content=await self._team_service.create_team(
                user_id=current_user.id, team_create_dto=team_create_dto
            ),
            status_code=201,
        )

    @patch(
        "/{team_id}",
        summary="Update team",
        status_code=200,
        responses={200: {"model": TeamDto}},
        dependencies=[],
    )
    async def update_team(
        self,
        *,
        team_update_dto: Annotated[TeamUpdateDto, Body(...)],
        team_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[TeamDto]:
        """Update a team"""
        return JSONResponse(
            content=await self._team_service.update_team(
                team_id=team_id, team_update_dto=team_update_dto
            ),
            status_code=200,
        )

    @delete(
        "/{team_id}",
        summary="Delete team",
        status_code=204,
        dependencies=[],
    )
    async def delete_team(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[None]:
        """Delete a team"""
        await self._team_service.delete_team(team_id=team_id)
        return JSONResponse.no_content()
