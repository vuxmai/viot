from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.database.repository import AsyncSqlalchemyRepository

from ..model.device_data_latest import DeviceDataLatest


class DeviceDataLatestRepository(AsyncSqlalchemyRepository):
    async def find_all_by_device_id_and_keys(
        self, device_id: UUID, keys: set[str]
    ) -> Sequence[DeviceDataLatest]:
        stmt = (
            select(DeviceDataLatest)
            .where(DeviceDataLatest.device_id == device_id)
            .where(DeviceDataLatest.key.in_(keys))
        )
        return (await self.session.execute(stmt)).scalars().all()

    async def find_all_keys_by_device_id(self, device_id: UUID) -> Sequence[str]:
        stmt = select(DeviceDataLatest.key).where(DeviceDataLatest.device_id == device_id)
        return (await self.session.execute(stmt)).scalars().all()
