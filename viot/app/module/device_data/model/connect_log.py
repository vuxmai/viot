from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import SMALLINT, TEXT, DateTime, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

from ..constants import ConnectStatus


class ConnectLog(Base):
    __tablename__ = "connect_logs"

    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        insert_default=lambda: datetime.now(UTC),
    )
    connect_status: Mapped[ConnectStatus] = mapped_column(SMALLINT)
    ip: Mapped[str] = mapped_column(TEXT)
    keep_alive: Mapped[int] = mapped_column(Integer)

    __table_args__ = (PrimaryKeyConstraint("device_id", "ts"),)
