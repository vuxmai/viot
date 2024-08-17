from enum import StrEnum


class TeamRole(StrEnum):
    OWNER = "Owner"
    ADMIN = "Admin"
    # MANAGER = "Manager"
    MEMBER = "Member"
    # BILLING_MANAGER = "Billing Manager"
    # DEVICE_OPERATOR = "Device Operator"
    VIEWER = "Viewer"


# Role descriptions and permissions can be defined in a separate constant or documentation
ROLE_DESCRIPTIONS = {
    TeamRole.OWNER: "Full control over team and all resources",
    TeamRole.ADMIN: "Manage team settings, members, and all resources",
    # TeamRole.MANAGER: "Manage devices, members, and most resources",
    TeamRole.MEMBER: "Access to devices and data with limited management",
    # TeamRole.BILLING_MANAGER: "Manage billing and subscriptions",
    # TeamRole.DEVICE_OPERATOR: "Operate and manage devices",
    TeamRole.VIEWER: "View-only access to devices and data",
}