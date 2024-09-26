from .base import Permission
from .permissions import (
    TeamInvitationPermissions,
    TeamMemberPermissions,
    TeamProfilePermissions,
)

__all__ = [
    "Permission",
    "ALL_PERMISSIONS",
    "MEMBER_PERMISSIONS",
    "TeamProfilePermissions",
    "TeamInvitationPermissions",
    "TeamMemberPermissions",
]

ALL_PERMISSIONS = [
    *TeamProfilePermissions.list_permissions(),
    *TeamInvitationPermissions.list_permissions(),
    *TeamMemberPermissions.list_permissions(),
]

MEMBER_PERMISSIONS = [
    TeamProfilePermissions.READ,
    TeamMemberPermissions.READ,
]
