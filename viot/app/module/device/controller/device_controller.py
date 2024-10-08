from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, get, post
from fastapi import Query
from fastapi.params import Path
from injector import inject

from app.common.controller import Controller
from app.common.dto.types import PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.auth.dependency import RequireTeamPermission
from app.module.auth.permission import TeamDevicePermission
from app.module.device.service.device_service import DeviceService

from ..constants import DeviceType
from ..dto.device_dto import DeviceCreateDto, DeviceDto, PagingDeviceDto


class DeviceController(Controller):
    @inject
    def __init__(self, device_service: DeviceService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/devices", tags=["Devices"], dependencies=[DependSession]
        )
        self._device_service = device_service

    @get(
        "",
        summary="Get all devices belong to team",
        status_code=200,
        responses={200: {"model": PagingDeviceDto}},
        dependencies=[RequireTeamPermission(TeamDevicePermission.READ)],
    )
    async def get_all_team_devices(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        page: PageQuery,
        page_size: PageSizeQuery,
        device_type: DeviceType = Query(
            None,
            alias="type",
            description="Filter by device type. 0 (Device), 1 (Gateway), 2 (Sub Device)",
        ),
    ) -> JSONResponse[PagingDeviceDto]:
        """Get all devices belong to team"""
        return JSONResponse(
            content=await self._device_service.get_all_devices_belong_to_team(
                team_id=team_id, page=page, page_size=page_size, device_type=device_type
            ),
            status_code=200,
        )

    @get(
        "/{device_id}",
        summary="Get device by id",
        status_code=200,
        responses={200: {"model": DeviceDto}},
        dependencies=[RequireTeamPermission(TeamDevicePermission.READ)],
    )
    async def get_device_by_id_and_team_id(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        device_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[DeviceDto]:
        """Get device by id"""
        return JSONResponse(
            content=await self._device_service.get_device_by_id_and_team_id(
                device_id=device_id, team_id=team_id
            ),
            status_code=200,
        )

    @post(
        "",
        summary="Create device",
        status_code=201,
        responses={201: {"model": DeviceDto}},
        dependencies=[RequireTeamPermission(TeamDevicePermission.MANAGE)],
    )
    async def create_device(
        self, *, team_id: Annotated[UUID, Path(...)], device_create_dto: DeviceCreateDto
    ) -> JSONResponse[DeviceDto]:
        """Create device"""
        return JSONResponse(
            content=await self._device_service.create_device(
                team_id=team_id, device_create_dto=device_create_dto
            ),
            status_code=201,
        )

    @delete(
        "/{device_id}",
        summary="Delete device by id and team id",
        status_code=204,
        dependencies=[RequireTeamPermission(TeamDevicePermission.DELETE)],
    )
    async def delete_device(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        device_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[None]:
        """Delete device"""
        await self._device_service.delete_device_by_id_and_team_id(
            device_id=device_id, team_id=team_id
        )
        return JSONResponse.no_content()
