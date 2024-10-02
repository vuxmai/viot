from app.common.dto import BaseOutDto

from ..model.permission import Permission


class PermissionDto(BaseOutDto):
    id: int
    scope: str
    title: str
    description: str | None

    @classmethod
    def from_model(cls, permission: Permission) -> "PermissionDto":
        return cls.model_validate(permission)
