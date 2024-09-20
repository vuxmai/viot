from uuid import UUID

from app.database.repository import PageableRepository

from ..model.device import Device


class DeviceRepository(PageableRepository[Device, UUID]):
    pass
