from datetime import datetime

from sqlalchemy import TEXT, Boolean, DateTime, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey

from ..constants import ViotUserRole


class User(Base, DateTimeMixin):
    __tablename__ = "users"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    first_name: Mapped[str] = mapped_column(TEXT)
    last_name: Mapped[str] = mapped_column(TEXT)
    email: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), init=False)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    role: Mapped[ViotUserRole] = mapped_column(TEXT)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
