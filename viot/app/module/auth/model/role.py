from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixin import DateTimeMixin


class Role(Base, DateTimeMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(init=False, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
