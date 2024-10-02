from uuid import UUID

from classy_fastapi import delete, get, post, put
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession

from ..dependency import RequireTeamPermission
from ..dto.role_dto import RoleCreateDto, RoleDto, RoleUpdateDto
from ..permission import TeamRolePermission
from ..service.team_role_service import TeamRoleService


class TeamRoleController(Controller):
    @inject
    def __init__(self, team_role_service: TeamRoleService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/roles", tags=["Team Roles"], dependencies=[DependSession]
        )
        self._team_role_service = team_role_service

    @get(
        "",
        summary="Get all roles of a team",
        status_code=200,
        responses={200: {"model": list[RoleDto]}},
        dependencies=[RequireTeamPermission(TeamRolePermission.READ)],
    )
    async def get_roles_by_team_id(self, *, team_id: UUID) -> JSONResponse[list[RoleDto]]:
        """Get all roles of a team"""
        return JSONResponse(
            content=await self._team_role_service.get_roles_by_team_id(team_id=team_id),
            status_code=200,
        )

    @post(
        "",
        summary="Create a role for a team",
        status_code=201,
        responses={201: {"model": RoleDto}},
        dependencies=[RequireTeamPermission(TeamRolePermission.MANAGE)],
    )
    async def create_role(
        self, *, team_id: UUID, role_create_dto: RoleCreateDto
    ) -> JSONResponse[RoleDto]:
        """Create a role for a team"""
        return JSONResponse(
            content=await self._team_role_service.create_role(
                team_id=team_id, role_create_dto=role_create_dto
            ),
            status_code=201,
        )

    @put(
        "/{role_id}",
        summary="Update a role of a team",
        status_code=200,
        responses={200: {"model": RoleDto}},
        dependencies=[RequireTeamPermission(TeamRolePermission.MANAGE)],
    )
    async def update_role(
        self, *, team_id: UUID, role_id: int, role_update_dto: RoleUpdateDto
    ) -> JSONResponse[RoleDto]:
        """Update a role of a team"""
        return JSONResponse(
            content=await self._team_role_service.update_role(
                team_id=team_id, role_id=role_id, role_update_dto=role_update_dto
            ),
            status_code=200,
        )

    @delete(
        "/{role_id}",
        summary="Delete a role of a team",
        status_code=204,
        dependencies=[RequireTeamPermission(TeamRolePermission.DELETE)],
    )
    async def delete_role(self, *, team_id: UUID, role_id: int) -> JSONResponse[None]:
        """Delete a role of a team"""
        await self._team_role_service.delete_role(role_id=role_id, team_id=team_id)
        return JSONResponse.no_content()
