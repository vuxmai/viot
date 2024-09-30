import msgspec


class Permission(msgspec.Struct, frozen=True):
    scope: str
    title: str
    description: str


class TeamProfilePermission:
    """
    Permissions for team profiles.
    """

    _PREFIX = "team:profile"

    READ = Permission(f"{_PREFIX}:read", "Read team profile", "Permission to read a team.")
    MANAGE = Permission(f"{_PREFIX}:manage", "Manage team profile", "Permission to manage a team.")
    DELETE = Permission(f"{_PREFIX}:delete", "Delete team profile", "Permission to delete a team.")


class TeamMemberPermission:
    """
    Permissions for team memberships.
    """

    _PREFIX = "team:memberships"

    READ = Permission(
        f"{_PREFIX}:read", "Read members", "Permission to read the members of a team."
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage", "Manage members", "Permission to manage the members of a team."
    )
    DELETE = Permission(
        f"{_PREFIX}:delete", "Delete member", "Permission to delete a member from a team."
    )


class TeamInvitationPermission:
    """
    Permissions for team invitations.
    """

    _PREFIX = "team:invitations"

    READ = Permission(
        f"{_PREFIX}:read", "Read Invitation", "Permission to read the invitations of a team."
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage", "Manage Invitation", "Permission to manage an invitation for a team."
    )
    REVOKE = Permission(
        f"{_PREFIX}:revoke", "Revoke Invitation", "Permission to revoke an invitation for a team."
    )


class TeamDevicePermission:
    """
    Permissions for team devices.
    """

    _PREFIX = "team:devices"

    READ = Permission(
        f"{_PREFIX}:read", "Read devices", "Permission to read the devices of a team."
    )
    MANAGE = Permission(
        f"{_PREFIX}:manage", "Manage devices", "Permission to manage the devices of a team."
    )
    DELETE = Permission(
        f"{_PREFIX}:delete", "Delete device", "Permission to delete a device from a team."
    )
