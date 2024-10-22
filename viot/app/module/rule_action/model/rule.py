from typing import Any
from uuid import UUID

from sqlalchemy import SMALLINT, TEXT, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey

from ..constants import EventType
from .action import Action
from .rule_action import RuleAction


class Rule(Base, DateTimeMixin):
    __tablename__ = "rules"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
    enable: Mapped[bool] = mapped_column(Boolean, insert_default=True)
    event_type: Mapped[EventType] = mapped_column(SMALLINT)
    sql: Mapped[str] = mapped_column(TEXT)  # SQL only use for EMQX, client don't need to know
    topic: Mapped[str] = mapped_column(TEXT)
    condition: Mapped[dict[str, Any]] = mapped_column(JSONB(none_as_null=True), insert_default={})
    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    actions: Mapped[list[Action]] = relationship(
        secondary=RuleAction.__tablename__, backref="rules", lazy="joined"
    )
