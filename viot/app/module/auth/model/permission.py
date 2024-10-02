from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(init=False, autoincrement=True, primary_key=True)
    scope: Mapped[str] = mapped_column(TEXT, unique=True, index=True)
    title: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
