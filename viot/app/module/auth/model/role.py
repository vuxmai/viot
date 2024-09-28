from uuid import UUID

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import DateTimeMixin


class Role(Base, DateTimeMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(init=False, autoincrement=True, primary_key=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
