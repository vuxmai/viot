from uuid import UUID

from injector import inject

from ..dto.device_attribute_dto import DeviceAttributeDto
from ..repository.device_attribute_repository import DeviceAttributeRepository


class DeviceAttributeService:
    @inject
    def __init__(
        self,
        device_attribute_repository: DeviceAttributeRepository,
    ) -> None:
        self._device_attribute_repository = device_attribute_repository

    async def get_all_keys(self, *, device_id: UUID) -> set[str]:
        keys = await self._device_attribute_repository.find_all_keys_by_device_id(
            device_id=device_id
        )
        return set(keys)

    async def get_all_by_device_id(
        self, *, device_id: UUID, keys: set[str]
    ) -> list[DeviceAttributeDto]:
        data = await self._device_attribute_repository.find_all_by_device_id_and_keys(
            device_id=device_id, keys=keys
        )
        return [DeviceAttributeDto.from_model(d) for d in data]
