from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import TEXT, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(TEXT, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        sort_order=999,
        init=False,
    )
