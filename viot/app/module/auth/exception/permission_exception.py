from app.common.exception import NotFoundException, PermissionDeniedException


class ResourceAccessDeniedException(PermissionDeniedException):
    def __init__(self) -> None:
        super().__init__(
            code="RESOURCE_ACCESS_DENIED",
            message="You are not allowed to access this resource",
        )


class PermissionNotFoundException(NotFoundException):
    def __init__(self, permission_scope: str) -> None:
        super().__init__(
            code="PERMISSION_NOT_FOUND",
            message=f"Permission with scope {permission_scope} not found",
        )
