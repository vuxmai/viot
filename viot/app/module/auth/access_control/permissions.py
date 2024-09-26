from .base import Permission, PermissionCategory


class TeamProfilePermissions(PermissionCategory):
    """
    Permissions for team profiles.
    """

    _PREFIX = "team:profile"

    READ = Permission(
        f"{_PREFIX}:read",
        "Read team profile",
        "Permission to read the profile of a team.",
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage",
        "Manage team profile",
        "Permission to manage the profile of a team.",
    )
    DELETE = Permission(
        f"{_PREFIX}:delete",
        "Delete team profile",
        "Permission to delete the profile of a team.",
    )

    @classmethod
    def get_permissions(cls) -> list[Permission]:
        return [cls.READ, cls.MANAGE]


class TeamMemberPermissions(PermissionCategory):
    """
    Permissions for team memberships.
    """

    _PREFIX = "team:memberships"

    READ = Permission(
        f"{_PREFIX}:read",
        "Read members",
        "Permission to read the members of an team.",
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage",
        "Manage members",
        "Permission to manage the members of an team.",
    )
    DELETE = Permission(
        f"{_PREFIX}:delete",
        "Delete member",
        "Permission to delete a member from a team.",
    )

    @classmethod
    def get_permissions(cls) -> list[Permission]:
        return [cls.READ, cls.MANAGE, cls.DELETE]


class TeamInvitationPermissions(PermissionCategory):
    """
    Permissions for team invitations.
    """

    _PREFIX = "team:invitations"

    READ = Permission(
        f"{_PREFIX}:read",
        "Read Invitation",
        "Permission to read the invitations of a team.",
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage",
        "Manage Invitation",
        "Permission to manage an invitation for a team.",
    )
    REVOKE = Permission(
        f"{_PREFIX}:revoke",
        "Revoke Invitation",
        "Permission to revoke an invitation for a team.",
    )

    @classmethod
    def get_permissions(cls) -> list[Permission]:
        return [cls.READ, cls.MANAGE, cls.REVOKE]
