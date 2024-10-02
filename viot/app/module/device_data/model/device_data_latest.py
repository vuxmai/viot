from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    DOUBLE_PRECISION,
    TEXT,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DeviceDataLatest(Base):
    __tablename__ = "device_data_latest"

    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    key: Mapped[str] = mapped_column(TEXT, primary_key=True)
    bool_v: Mapped[bool | None] = mapped_column(BOOLEAN)
    str_v: Mapped[str | None] = mapped_column(TEXT)
    long_v: Mapped[int | None] = mapped_column(BIGINT)
    double_v: Mapped[float | None] = mapped_column(DOUBLE_PRECISION)
    json_v: Mapped[dict[str, Any] | None] = mapped_column(JSON(none_as_null=True))

    __table_args__ = (
        Index("device_data_latest_device_id_idx", "device_id"),
        Index("device_data_latest_device_id_key_idx", "device_id", "key"),
    )

    @property
    def value(self) -> bool | str | int | float | dict[str, Any] | None:
        if self.bool_v is not None:
            return self.bool_v
        if self.str_v is not None:
            return self.str_v
        if self.long_v is not None:
            return self.long_v
        if self.double_v is not None:
            return self.double_v
        if self.json_v is not None:
            return self.json_v
        return None
