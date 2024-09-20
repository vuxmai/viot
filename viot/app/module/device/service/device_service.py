from uuid import UUID

from injector import inject

from app.database.repository import Filter, Pageable
from app.module.team.exception.team_exception import TeamNotFoundException
from app.module.team.repository.team_repository import TeamRepository

from ..constants import DeviceType
from ..dto.device_dto import DeviceCreateDto, DeviceDto, PagingDeviceDto
from ..exception.device_exception import DeviceNotFoundException
from ..model.device import Device
from ..repository.device_repository import DeviceRepository


class DeviceService:
    @inject
    def __init__(
        self,
        device_repository: DeviceRepository,
        team_repository: TeamRepository,
    ) -> None:
        self._device_repository = device_repository
        self._team_repository = team_repository

    async def get_device_by_id_and_team_id(self, *, device_id: UUID, team_id: UUID) -> DeviceDto:
        device = await self._device_repository.find_by_device_id_and_team_id(device_id, team_id)
        if device is None:
            raise DeviceNotFoundException(device_id)
        return DeviceDto.from_model(device)

    async def get_all_devices_belong_to_team(
        self, *, team_id: UUID, page: int, page_size: int, device_type: DeviceType | None
    ) -> PagingDeviceDto:
        filters = [Filter(field="team_id", operator="eq", value=team_id)]
        if device_type is not None:
            filters.append(Filter(field="device_type", operator="eq", value=device_type))
        pageable = Pageable(page=page, page_size=page_size, filters=filters)
        device_page = await self._device_repository.find_all_with_paging(pageable)
        return PagingDeviceDto.from_page(device_page)

    async def create_device(
        self, *, team_id: UUID, device_create_dto: DeviceCreateDto
    ) -> DeviceDto:
        team = await self._team_repository.exists_by_id(team_id)
        if not team:
            raise TeamNotFoundException
        device = Device(
            team_id=team_id,
            name=device_create_dto.name,
            device_type=device_create_dto.device_type,
            description=device_create_dto.description,
        )
        device = await self._device_repository.save(device)
        return DeviceDto.from_model(device)

    async def delete_device_by_id_and_team_id(self, *, device_id: UUID, team_id: UUID) -> None:
        await self._device_repository.delete_by_device_id_and_team_id(device_id, team_id)
