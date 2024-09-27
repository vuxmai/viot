from app.common.exception import NotFoundException, PermissionDeniedException


class ResourceAccessDeniedException(PermissionDeniedException):
    def __init__(self) -> None:
        super().__init__(
            code="RESOURCE_ACCESS_DENIED",
            message="You are not allowed to access this resource",
        )


class PermissionsNotFoundException(NotFoundException):
    def __init__(self, permission_scopes: list[str]) -> None:
        formatted_scopes = ", ".join(f"'{scope}'" for scope in permission_scopes)
        super().__init__(
            code="PERMISSION_NOT_FOUND",
            message=f"Permissions not found for the following scope(s): {formatted_scopes}",
        )
