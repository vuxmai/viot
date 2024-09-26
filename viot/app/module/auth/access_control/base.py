from abc import ABC, abstractmethod

import msgspec


class Permission(msgspec.Struct, frozen=True):
    scope: str
    title: str
    description: str


class PermissionCategory(ABC):
    """
    Base class for a category of permissions.
    """

    _SCOPE_PREFIX: str

    @classmethod
    @abstractmethod
    def list_permissions(cls) -> list[Permission]:
        """Return all permissions for this category."""
        pass
