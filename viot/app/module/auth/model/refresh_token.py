from datetime import datetime
from uuid import UUID

from sqlalchemy import TEXT, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(TEXT, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default_factory=lambda: datetime.now().replace(tzinfo=None),
        sort_order=999,
        init=False,
    )
