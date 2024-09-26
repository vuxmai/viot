from app.common.dto import BaseInDto


class RoleCreateDto(BaseInDto):
    name: str
    description: str | None
    scopes: set[str]
