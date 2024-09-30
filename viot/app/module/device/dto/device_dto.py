from datetime import datetime
from typing import Any
from uuid import UUID

from app.common.dto import BaseOutDto, PagingDto
from app.common.dto.base import BaseInDto
from app.database.repository.pagination import Page

from ..constants import DeviceStatus, DeviceType
from ..model.device import Device


class DeviceCreateDto(BaseInDto):
    name: str
    description: str
    device_type: DeviceType


class DeviceDto(BaseOutDto):
    id: UUID
    name: str
    description: str
    device_type: DeviceType
    token: str
    status: DeviceStatus
    image_url: str | None
    disabled: bool
    last_connection: datetime | None
    meta_data: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, device: Device) -> "DeviceDto":
        return cls.model_validate(device)


class PagingDeviceDto(PagingDto[DeviceDto]):
    @classmethod
    def from_page(cls, page: Page[Device]) -> "PagingDeviceDto":
        return cls(
            items=[DeviceDto.from_model(device) for device in page.items],
            total_items=page.total_items,
            page=page.page,
            page_size=page.page_size,
        )
