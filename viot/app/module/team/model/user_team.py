from uuid import UUID

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class UserTeam(Base):
    __tablename__ = "users_teams"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(TEXT)
