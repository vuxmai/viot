from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TEXT, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixin import DateTimeMixin, PrimaryKey

if TYPE_CHECKING:
    from app.module.user.model import User


class Team(Base, DateTimeMixin):
    __tablename__ = "teams"

    id: Mapped[PrimaryKey] = mapped_column(init=False)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(TEXT)
    slug: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(TEXT)
    default: Mapped[bool] = mapped_column(Boolean)

    users: Mapped[list["User"]] = relationship(
        secondary="users_teams", back_populates="teams", init=False
    )


class UserTeam(Base):
    __tablename__ = "users_teams"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(TEXT)
