from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.orm.session import Session

from app.models import Permission, Role, RolePermission
from app.module.auth.constants import TEAM_ROLE_OWNER


def get_role_owner_ids(session: Session) -> Sequence[int]:
    return session.execute(select(Role.id).where(Role.name == TEAM_ROLE_OWNER)).scalars().all()


def get_permission_ids_by_scopes(session: Session, scopes: Sequence[str]) -> Sequence[int]:
    return (
        session.execute(select(Permission.id).where(Permission.scope.in_(scopes))).scalars().all()
    )


def save_permissions(session: Session, permissions: list[Permission]) -> None:
    session.add_all(permissions)
    session.flush()


def update_owner_permissions(
    session: Session, role_owner_ids: Sequence[int], permissions: Sequence[Permission]
) -> None:
    values: list[dict[str, Any]] = []
    for permission in permissions:
        for role_id in role_owner_ids:
            values.append({"role_id": role_id, "permission_id": permission.id})

    if values:
        stmt = insert(RolePermission).values(values)
        session.execute(stmt)


def remove_owner_permissions(
    session: Session, role_owner_ids: Sequence[int], permission_ids: Sequence[int]
) -> None:
    stmt = delete(RolePermission).where(
        RolePermission.role_id.in_(role_owner_ids),
        RolePermission.permission_id.in_(permission_ids),
    )
    session.execute(stmt)


def delete_permissions(session: Session, permission_ids: Sequence[int]) -> None:
    stmt = delete(Permission).where(Permission.id.in_(permission_ids))
    session.execute(stmt)
