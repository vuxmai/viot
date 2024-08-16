from datetime import datetime

from sqlalchemy import TEXT, Boolean, DateTime, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixin import DateTimeMixin, PrimaryKey
from app.module.team.model import Team

from .constant import ViotUserRole


class User(Base, DateTimeMixin):
    __tablename__ = "users"

    id: Mapped[PrimaryKey] = mapped_column(init=False)
    first_name: Mapped[str] = mapped_column(TEXT)
    last_name: Mapped[str] = mapped_column(TEXT)
    email: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime, init=False)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    role: Mapped[ViotUserRole] = mapped_column(TEXT, default=ViotUserRole.USER)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    teams: Mapped[list[Team]] = relationship(
        secondary="users_teams", back_populates="users", init=False
    )

    @hybrid_property
    def verified(self) -> bool:
        return self.email_verified_at is not None
