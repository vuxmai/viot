from datetime import UTC, datetime

from sqlalchemy import TEXT, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PasswordReset(Base):
    __tablename__ = "password_resets"

    email: Mapped[str] = mapped_column(TEXT, primary_key=True)
    token: Mapped[str] = mapped_column(TEXT, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), init=False
    )
