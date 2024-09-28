from datetime import datetime

from app.common.dto import BaseInDto, BaseOutDto

from ..model.role import Role


class RoleCreateDto(BaseInDto):
    name: str
    description: str | None
    scopes: set[str]


class RoleDto(BaseOutDto):
    id: int
    name: str
    description: str | None
    scopes: set[str]
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, role: Role, scopes: set[str]) -> "RoleDto":
        return cls(
            id=role.id,
            name=role.name,
            description=role.description,
            scopes=scopes,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )
