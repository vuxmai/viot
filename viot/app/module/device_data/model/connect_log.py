from datetime import datetime
from uuid import UUID

from sqlalchemy import SMALLINT, TEXT, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

from ..constants import ConnectStatus


class ConnectLog(Base):
    __tablename__ = "connect_logs"

    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    connect_status: Mapped[ConnectStatus] = mapped_column(SMALLINT)
    ip: Mapped[str] = mapped_column(TEXT)

    __table_args__ = (PrimaryKeyConstraint("device_id", "ts"),)
