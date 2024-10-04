from datetime import datetime
from typing import Any

from app.common.dto import BaseOutDto

from ..model.device_attribute import DeviceAttribute


class DeviceAttributeDto(BaseOutDto):
    last_update: datetime
    key: str
    value: Any
    device_can_edit: bool

    @classmethod
    def from_model(cls, model: DeviceAttribute) -> "DeviceAttributeDto":
        return cls(
            last_update=model.last_update,
            key=model.key,
            value=model.value,
            device_can_edit=model.device_can_edit,
        )
