from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, delete

from app.database.repository import PageableRepository

from ..model.connect_log import ConnectLog


class ConnectLogRepository(PageableRepository[ConnectLog, tuple[UUID, datetime]]):
    async def delete_by_device_id_and_date_range(
        self,
        *,
        device_id: UUID,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> None:
        conditions = [ConnectLog.device_id == device_id]
        if start_date:
            conditions.append(ConnectLog.ts >= start_date)
        if end_date:
            conditions.append(ConnectLog.ts <= end_date)

        stmt = delete(ConnectLog).where(and_(*conditions))
        await self.session.execute(stmt)
