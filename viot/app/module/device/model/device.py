import uuid
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import SMALLINT, TEXT, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey

from ..constants import DeviceStatus, DeviceType, UplinkProtocol


class Device(Base, DateTimeMixin):
    __tablename__ = "devices"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(TEXT, unique=True)
    description: Mapped[str] = mapped_column(TEXT)
    device_type: Mapped[DeviceType] = mapped_column(SMALLINT)
    token: Mapped[str] = mapped_column(TEXT, insert_default=lambda: uuid.uuid4().hex, init=False)
    status: Mapped[DeviceStatus] = mapped_column(
        SMALLINT, insert_default=DeviceStatus.OFFLINE, init=False
    )
    image_url: Mapped[str | None] = mapped_column(TEXT, init=False)
    disabled: Mapped[bool] = mapped_column(Boolean, insert_default=False, init=False)
    last_connection: Mapped[datetime | None] = mapped_column(DateTime, init=False)
    meta_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, init=False)
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": DeviceType.DEVICE,
    }


class Gateway(Device):
    __tablename__ = "gateways"

    id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", onupdate="CASCADE", ondelete="CASCADE"),
        init=False,
        primary_key=True,
    )
    devices: Mapped[list["SubDevice"]] = relationship(
        back_populates="gateway", foreign_keys="[SubDevice.gateway_id]", init=False
    )

    __mapper_args__ = {"polymorphic_identity": DeviceType.GATEWAY}


class SubDevice(Device):
    __tablename__ = "sub_devices"

    id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", onupdate="CASCADE", ondelete="CASCADE"),
        init=False,
        primary_key=True,
    )
    uplink_protocol: Mapped[UplinkProtocol] = mapped_column(SMALLINT)
    gateway_id: Mapped[UUID] = mapped_column(
        ForeignKey("gateways.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    gateway: Mapped[Gateway] = relationship(
        back_populates="devices", foreign_keys=[gateway_id], init=False
    )

    __mapper_args__ = {"polymorphic_identity": DeviceType.SUB_DEVICE}
