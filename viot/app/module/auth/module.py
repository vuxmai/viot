from injector import Binder, Module, SingletonScope

from .controller.auth_controller import AuthController
from .controller.user_controller import UserController
from .repository.password_reset_repository import PasswordResetRepository
from .repository.refresh_token_repository import RefreshTokenRepository
from .repository.user_repository import UserRepository
from .service.auth_service import AuthService
from .service.user_service import UserService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(RefreshTokenRepository, RefreshTokenRepository, SingletonScope)
        binder.bind(PasswordResetRepository, PasswordResetRepository, SingletonScope)
        binder.bind(UserRepository, UserRepository, SingletonScope)

        binder.bind(AuthService, AuthService, SingletonScope)
        binder.bind(UserService, UserService, SingletonScope)

        binder.bind(AuthController, AuthController, SingletonScope)
        binder.bind(UserController, UserController, SingletonScope)
