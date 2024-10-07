from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from app.database.repository import AsyncSqlalchemyRepository
from app.database.repository.pagination import SortDirection

from ..model.device_data import DeviceData


class DeviceDataRepository(AsyncSqlalchemyRepository):
    async def find_data_by_device_id_and_keys(
        self,
        *,
        device_id: UUID,
        keys: set[str],
        start_date: datetime,
        end_date: datetime,
        limit: int,
        order_by: SortDirection | None = None,
    ) -> Sequence[DeviceData]:
        stmt = select(DeviceData).filter(
            DeviceData.device_id == device_id,
            DeviceData.key.in_(keys),
            DeviceData.ts >= start_date,
            DeviceData.ts <= end_date,
        )
        if order_by:
            stmt = stmt.order_by(
                DeviceData.ts.desc() if order_by == "desc" else DeviceData.ts.asc()
            )
        stmt = stmt.limit(limit)

        return (await self.session.execute(stmt)).scalars().all()
