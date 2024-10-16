from datetime import datetime
from uuid import UUID

from app.common.dto import BaseInDto


class DeviceConnectedEventDto(BaseInDto):
    device_id: UUID


class DeviceDisconnectedEventDto(BaseInDto):
    device_id: UUID
    ip_address: str
    disconnected_at: datetime
