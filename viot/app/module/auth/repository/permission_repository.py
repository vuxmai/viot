from ..access_control import ALL_PERMISSIONS, ALL_PERMISSIONS_DICT, Permission


class PermissionRepository:
    def find_all_permissions(self) -> list[Permission]:
        return ALL_PERMISSIONS

    def find_permission_by_scope(self, scope: str) -> Permission | None:
        return ALL_PERMISSIONS_DICT.get(scope)
