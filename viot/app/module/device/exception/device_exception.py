from uuid import UUID

from app.common.exception import NotFoundException


class DeviceNotFoundException(NotFoundException):
    def __init__(self, device_id: UUID) -> None:
        super().__init__(message=f"Device with id {device_id} not found")
