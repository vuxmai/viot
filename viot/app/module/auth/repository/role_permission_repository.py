from app.database.repository import CrudRepository
from app.module.auth.model.role_permission import RolePermission


class RolePermissionRepository(CrudRepository[RolePermission, tuple[int, int]]):
    pass
