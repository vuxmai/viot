from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, select

from app.database.repository import AsyncSqlalchemyRepository

from ..model.device_attribute import DeviceAttribute


class DeviceAttributeRepository(AsyncSqlalchemyRepository):
    async def find_all_keys_by_device_id(self, device_id: UUID) -> Sequence[str]:
        stmt = select(DeviceAttribute.key).where(DeviceAttribute.device_id == device_id)
        return (await self.session.execute(stmt)).scalars().all()

    async def find_all_by_device_id_and_keys(
        self, device_id: UUID, keys: set[str]
    ) -> Sequence[DeviceAttribute]:
        stmt = (
            select(DeviceAttribute)
            .where(DeviceAttribute.device_id == device_id)
            .where(DeviceAttribute.key.in_(keys))
        )
        return (await self.session.execute(stmt)).scalars().all()

    async def delete_by_keys(self, device_id: UUID, keys: set[str]) -> None:
        stmt = (
            delete(DeviceAttribute)
            .where(DeviceAttribute.device_id == device_id)
            .where(DeviceAttribute.key.in_(keys))
        )
        await self.session.execute(stmt)
