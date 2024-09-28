from app.common.exception import BadRequestException


class AssignSensitiveRoleException(BadRequestException):
    def __init__(self, role_name: str) -> None:
        super().__init__(
            code="ASSIGN_ROLE_SENSITIVE",
            message=f"Role {role_name} is sensitive and cannot be assigned to a member",
        )
