from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import TEXT, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import UUIDPrimaryKey


class TeamInvitation(Base):
    __tablename__ = "team_invitations"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    inviter_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(TEXT)
    role: Mapped[str] = mapped_column(TEXT)
    token: Mapped[str] = mapped_column(
        TEXT, nullable=False, insert_default=lambda: uuid4().hex, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), init=False
    )
