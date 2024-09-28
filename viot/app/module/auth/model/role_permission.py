from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RolePermission(Base):
    __tablename__ = "roles_permissions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"))

    __table_args__ = (PrimaryKeyConstraint("role_id", "permission_id"),)
