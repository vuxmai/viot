from datetime import datetime

from app.common.dto import BaseInDto, BaseOutDto


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
