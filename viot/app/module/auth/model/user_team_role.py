from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import create_view  # type: ignore
from sqlalchemy_utils.view import CreateView, DropView  # type: ignore

from app.database.base import Base

from .permission import Permission
from .role_permission import RolePermission


class UserTeamRole(Base):
    __tablename__ = "users_teams_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), init=False
    )
    __table_args__ = (PrimaryKeyConstraint("user_id", "role_id", "team_id"),)


class UserTeamPermissionScopeView(Base):
    __tablename__ = "vw_user_team_permission_scope"

    selectable = (
        select(
            UserTeamRole.user_id, UserTeamRole.team_id, Permission.scope.label("permission_scope")
        )
        .join(RolePermission, RolePermission.role_id == UserTeamRole.role_id)
        .join(Permission, RolePermission.permission_id == Permission.id)
    )
    __table__ = create_view(name=__tablename__, selectable=selectable, metadata=Base.metadata)

    @classmethod
    def create(cls, op: Any) -> None:
        op.execute(CreateView(cls.__tablename__, cls.selectable))

    @classmethod
    def drop(cls, op: Any) -> None:
        op.execute(DropView(cls.__tablename__))
