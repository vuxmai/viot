from injector import Binder, Module, SingletonScope

from .controller.auth_controller import AuthController
from .controller.user_controller import UserController
from .repository.password_reset_repository import PasswordResetRepository
from .repository.refresh_token_repository import RefreshTokenRepository
from .repository.role_permission_repository import RolePermissionRepository
from .repository.role_repository import RoleRepository
from .repository.user_repository import UserRepository
from .repository.user_team_role_repository import UserTeamRoleRepository
from .service.auth_service import AuthService
from .service.permission_service import PermissionService
from .service.user_service import UserService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(RefreshTokenRepository, RefreshTokenRepository, SingletonScope)
        binder.bind(PasswordResetRepository, PasswordResetRepository, SingletonScope)
        binder.bind(UserRepository, UserRepository, SingletonScope)
        binder.bind(UserTeamRoleRepository, UserTeamRoleRepository, SingletonScope)
        binder.bind(RoleRepository, RoleRepository, SingletonScope)
        binder.bind(RolePermissionRepository, RolePermissionRepository, SingletonScope)

        binder.bind(AuthService, AuthService, SingletonScope)
        binder.bind(UserService, UserService, SingletonScope)
        binder.bind(PermissionService, PermissionService, SingletonScope)

        binder.bind(AuthController, AuthController, SingletonScope)
        binder.bind(UserController, UserController, SingletonScope)
