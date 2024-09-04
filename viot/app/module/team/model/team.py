from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TEXT, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.module.auth.model.user import User


class Team(Base, DateTimeMixin):
    __tablename__ = "teams"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(TEXT)
    slug: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(TEXT)
    default: Mapped[bool] = mapped_column(Boolean)

    users: Mapped[list["User"]] = relationship(
        secondary="users_teams", back_populates="teams", init=False
    )
