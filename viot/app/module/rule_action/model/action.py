from typing import Any
from uuid import UUID

from sqlalchemy import SMALLINT, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey

from ..constants import ActionType


class Action(Base, DateTimeMixin):
    __tablename__ = "actions"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
    action_type: Mapped[ActionType] = mapped_column(SMALLINT)
    config: Mapped[dict[str, Any]] = mapped_column(JSONB(none_as_null=True), insert_default={})
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", onupdate="CASCADE", ondelete="CASCADE")
    )
