from datetime import datetime
from uuid import uuid4

from sqlalchemy import TEXT, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PasswordReset(Base):
    __tablename__ = "password_resets"

    email: Mapped[str] = mapped_column(TEXT, primary_key=True)
    token: Mapped[str] = mapped_column(
        TEXT, nullable=False, insert_default=lambda: uuid4().hex, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=lambda: datetime.now().replace(tzinfo=None), init=False
    )
