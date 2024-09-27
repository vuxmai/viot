from sqlalchemy import TEXT, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import DateTimeMixin, UUIDPrimaryKey


class Team(Base, DateTimeMixin):
    __tablename__ = "teams"

    id: Mapped[UUIDPrimaryKey] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(TEXT)
    slug: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(TEXT)
    default: Mapped[bool] = mapped_column(Boolean)
